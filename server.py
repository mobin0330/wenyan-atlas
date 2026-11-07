#!/usr/bin/env python3
"""Two separate entry modes: public-fixture preview or SDK-gated private site."""
import argparse,json,mimetypes,os,sys,tempfile,threading,time
from collections import deque
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
from atlas import Atlas,ROOT,scopes

STATIC={'/':'index.html','/app.js':'app.js','/style.css':'style.css','/manifest.webmanifest':'manifest.webmanifest','/icon.svg':'icon.svg'}

class Business:
    def send_bytes(self,status,data,typ='application/json; charset=utf-8'):
        self.send_response(status);self.send_header('Content-Type',typ);self.send_header('Content-Length',str(len(data)))
        if self.server.preview:
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'")
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
        else:self.headers_common()
        self.end_headers(); self.wfile.write(data)
    def json(self,status,obj):self.send_bytes(status,json.dumps(obj,ensure_ascii=False).encode())
    def log_message(self,*args):pass
    def limited(self):
        with self.server.rate_lock:
            now=time.monotonic();q=self.server.requests
            while q and q[0]<now-60:q.popleft()
            if len(q)>=240:self.json(429,{'error':'请求过于频繁，请稍后重试。'});return True
            q.append(now)
        return False
    def route(self):
        try:
            u=urlsplit(self.path);q=parse_qs(u.query);mode=q.get('mode',['sample' if self.server.preview else 'published'])[0]
            sample=self.server.preview and mode=='sample'
            selected=scopes(q.get('scopes',['小学'])[0].split(','));a=self.server.atlas
            if self.command=='GET':
                if u.path in STATIC:
                    f=ROOT/'static'/STATIC[u.path];self.send_bytes(200,f.read_bytes(),mimetypes.guess_type(f)[0] or 'application/octet-stream');return
                if u.path=='/api/guide':self.json(200,json.loads((ROOT/'data/user-guide.json').read_text()));return
                if u.path.startswith('/api/handbook/'):
                    docs={'manual':'STUDENT-MANUAL.md','whitepaper':'PRODUCT-WHITEPAPER.md','provenance':'LEXICAL-PROVENANCE.md'}
                    name=docs.get(u.path.rsplit('/',1)[-1])
                    if not name:self.json(404,{'error':'文档不存在'});return
                    self.send_bytes(200,(ROOT/'docs'/name).read_bytes(),'text/markdown; charset=utf-8');return
                if u.path=='/api/bootstrap':
                    self.json(200,{'preview':self.server.preview,'scopes':list(scopes(['小学','六年级','七年级','八年级','九年级'])),'coverage':a.coverage(),'corpus':a.corpus(selected,sample),'saved_scopes':['小学'] if self.server.preview else a.preferences('household')});return
                if u.path=='/api/graph':self.json(200,a.graph(q.get('lexeme',['zhi'])[0],selected,sample,q.get('sense',[None])[0]));return
                if u.path=='/api/records':self.json(200,{'records':[] if self.server.preview else a.records('household')});return
                if u.path=='/api/health':self.json(200,{'ok':True,'version':'0.1.0','mode':'public-fixture-preview' if self.server.preview else 'private'});return
            elif self.command=='POST':
                body=self.payload
                if u.path=='/api/attempt':self.json(200,a.answer(body.get('question_id'),body.get('choice'),body.get('hinted',False),selected,sample,None if self.server.preview else 'household'));return
                if self.server.preview:self.json(405,{'error':'样例服务不保存个人数据。体验记录只在当前浏览器保存。'});return
                if u.path=='/api/preferences':self.json(200,{'scopes':a.preferences('household',body.get('scopes'))});return
                if u.path=='/api/read':a.read('household',body.get('work_id'),selected);self.json(200,{'ok':True});return
            self.json(404,{'error':'未找到该内容。'})
        except (ValueError,TypeError,json.JSONDecodeError) as e:self.json(400,{'error':str(e)})
        except Exception:
            self.json(500,{'error':'服务暂时不可用，请重试；如持续失败，请检查服务日志。'})
            print('Business request failed; details withheld from browser.',file=sys.stderr)

class PreviewHandler(Business,BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.limited():self.route()
    def do_POST(self):
        if self.limited():return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=16384:raise ValueError('请求大小不正确')
            self.payload=json.loads(self.rfile.read(size))
            if not isinstance(self.payload,dict):raise ValueError('需要 JSON 对象')
        except (ValueError,TypeError):self.json(400,{'error':'请求无效'});return
        self.route()


def build_server(port,private=False,db=None):
    if private:
        # Import the actual shared module, never copy its implementation into this project.
        sdk=Path(os.environ.get('SECURITY_SERVICE_DIR',str(ROOT.parents[1]/'security-service')))
        sys.path.insert(0,str(sdk))
        from shared_email_auth import GateConfig,EmailGate
        from shared_email_auth.http import EmailHTTPMixin
        origin=os.environ.get('ATLAS_ORIGIN');client=os.environ.get('ATLAS_CLIENT_FILE')
        if not origin or not client:raise SystemExit('私有模式需设置 ATLAS_ORIGIN（HTTPS）及 ATLAS_CLIENT_FILE；不会回退免登录。')
        gate=EmailGate(GateConfig(public_origin=origin,client_file=Path(client),title='文言星图',mark='文',description='关联原文、理解用法、持续复习。',protected_prefixes=('/api/',)))
        class PrivateHandler(Business,EmailHTTPMixin,BaseHTTPRequestHandler):
            def do_GET(self):
                if self.limited() or self.email_handle():return
                self.route()
            def do_POST(self):
                if self.limited() or self.email_handle():return
                self.payload=self.email_payload;self.route()
        handler=PrivateHandler;atlas=Atlas(db or ROOT/'.local/atlas.sqlite');tmp=None
    else:
        # Always seed a fresh fixture database. A preview can NEVER open the private database.
        if db:raise SystemExit('预览模式禁止指定数据库。')
        tmp=tempfile.TemporaryDirectory(prefix='wenyan-public-preview-');atlas=Atlas(Path(tmp.name)/'sample.sqlite');atlas.import_file(ROOT/'data/sample.json');handler=PreviewHandler
    server=ThreadingHTTPServer(('127.0.0.1',port),handler);server.daemon_threads=True
    server.preview=not private;server.atlas=atlas;server.fixture_temp=tmp;server.requests=deque();server.rate_lock=threading.Lock()
    if private:server.email_gate=gate
    return server

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9381);p.add_argument('--private',action='store_true');p.add_argument('--db',type=Path);args=p.parse_args()
    server=build_server(args.port,args.private,args.db)
    print(f'文言星图 {"私有服务（仅经 HTTPS 入口访问）" if args.private else "公开样例本地预览"}：http://127.0.0.1:{args.port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:
        server.server_close()
        if server.fixture_temp:server.fixture_temp.cleanup()
