"""Private trial deployment, authenticated by the shared SDK ASGI adapter."""
import asyncio,json,mimetypes,os,sys,time
from collections import deque
from pathlib import Path
from urllib.parse import parse_qs
from atlas import Atlas,ROOT,scopes
sys.path.insert(0,str(ROOT.parents[1]/'security-service'))
from shared_email_auth import GateConfig
from shared_email_auth.asgi import EmailAuthMiddleware
from server import STATIC
from curriculum import EVIDENCE,LINKS,enrich
import recitation
PLAN=json.loads((ROOT/'data/reading-plan.json').read_text())
for entry in PLAN:
 if entry['work_id'] in LINKS:entry['scope']={6:'六年级',7:'七年级'}[LINKS[entry['work_id']]['book']['grade']]
class TrialAtlas(Atlas):
 def corpus(self,selected=None,sample=False):
  d=super().corpus(selected,True if sample else False)
  if not sample:return enrich(d)
  wanted=set(scopes(selected or ['小学']));ids={p['work_id'] for p in PLAN if p['scope'] in wanted}
  d['works']=[w for w in d['works'] if w['id'] in ids];wids={w['id'] for w in d['works']}
  d['sentences']=[s for s in d['sentences'] if s['work_id'] in wids];sids={s['id']for s in d['sentences']}
  d['occurrences']=[o for o in d['occurrences'] if o['sentence_id'] in sids];oids={o['id'] for o in d['occurrences']};sens={o['sense_id'] for o in d['occurrences']};lex={o['lexeme_id'] for o in d['occurrences']}
  d['senses']=[s for s in d['senses'] if s['id'] in sens];d['lexemes']=[l for l in d['lexemes'] if l['id'] in lex];d['questions']=[q for q in d['questions'] if q['occurrence_id'] in oids]
  return enrich(d)
atlas=TrialAtlas(ROOT/'.local/trial-v4.sqlite');requests=deque()
async def business(scope,receive,send):
 if scope['type']=='lifespan':
  while True:
   m=await receive()
   if m['type']=='lifespan.startup':await send({'type':'lifespan.startup.complete'})
   elif m['type']=='lifespan.shutdown':await send({'type':'lifespan.shutdown.complete'});return
  return
 if scope['type']!='http':return
 status=200;typ='application/json; charset=utf-8';method=scope['method'];path=scope['path'];q=parse_qs(scope['query_string'].decode());sample=q.get('mode',['trial'])[0]!='published'
 try:
  now=time.monotonic()
  while requests and requests[0]<now-60:requests.popleft()
  if len(requests)>600:status=429;out={'error':'操作过于频繁，请稍后再试。'}
  else:
   requests.append(now);selected=scopes(q.get('scopes',['小学'])[0].split(','));body={}
   if method=='POST':
    raw=b''
    while True:
     e=await receive()
     if e['type']=='http.disconnect':return
     raw+=e.get('body',b'')
     if len(raw)>16384:raise ValueError('请求过大')
     if not e.get('more_body'):break
    body=json.loads(raw)
    if not isinstance(body,dict):raise ValueError('需要 JSON 对象')
   if method=='GET' and path in STATIC:
    f=ROOT/'static'/STATIC[path];out=f.read_bytes();typ=mimetypes.guess_type(f)[0]or'application/octet-stream'
   elif method=='GET' and path=='/api/bootstrap':out={'preview':False,'trial':True,'saved_scopes':atlas.preferences('household'),'coverage':atlas.coverage(),'corpus':atlas.corpus(selected,sample),'curriculum':EVIDENCE,'scopes':list(scopes(['小学','六年级','七年级','八年级','九年级']))}
   elif method=='GET' and path=='/api/graph':out=atlas.graph(q.get('lexeme',['zhi'])[0],selected,sample,q.get('sense',[None])[0])
   elif method=='GET' and path=='/api/work-status':out=json.loads((ROOT/'data/work-status.json').read_text())
   elif method=='GET' and path=='/api/guide':out=json.loads((ROOT/'data/user-guide.json').read_text())
   elif method=='GET' and path.startswith('/api/handbook/'):
    docs={'manual':'STUDENT-MANUAL.md','whitepaper':'PRODUCT-WHITEPAPER.md','provenance':'LEXICAL-PROVENANCE.md','textbooks':'TEXTBOOK-RESEARCH.md','textbook-directories':'TEXTBOOK-DIRECTORIES.md','textbook-inventory':'TEXTBOOK-CONTENT-INVENTORY.csv'}
    name=docs.get(path.rsplit('/',1)[-1])
    if not name:raise ValueError('文档不存在')
    out=(ROOT/'docs'/name).read_bytes();typ=('text/csv'if name.endswith('.csv')else'text/markdown')+'; charset=utf-8'
   elif method=='GET' and path in ('/api/textbooks','/api/textbooks/content','/api/textbooks/requirements'):
    name={'/api/textbooks':'textbook-register.json','/api/textbooks/content':'textbook-content-inventory.json','/api/textbooks/requirements':'textbook-learning-requirements.json'}[path]
    out=json.loads((ROOT/'data'/name).read_text())
   elif method=='GET' and path=='/api/recitation':out={'records':recitation.records(atlas,'household')}
   elif method=='POST' and path=='/api/recitation':out=recitation.save(atlas,'household',body,selected,sample)
   elif method=='GET' and path=='/api/records':out={'records':atlas.records('household')}
   elif method=='GET' and path=='/api/health':out={'ok':True,'version':'0.3.0','mode':'authenticated-trial'}
   elif method=='POST' and path=='/api/preferences':out={'scopes':atlas.preferences('household',body.get('scopes'))}
   elif method=='POST' and path=='/api/attempt':out=atlas.answer(body.get('question_id'),body.get('choice'),body.get('hinted',False),selected,sample,'household')
   elif method=='POST' and path=='/api/read':atlas.read('household',body.get('work_id'),selected,sample);out={'ok':True}
   else:status=404;out={'error':'未找到该内容'}
 except (ValueError,TypeError) as e:status=400;out={'error':str(e)}
 except Exception:status=503;out={'error':'服务暂时不可用，请稍后再试。'}
 data=out if isinstance(out,bytes)else json.dumps(out,ensure_ascii=False).encode()
 await send({'type':'http.response.start','status':status,'headers':[(b'content-type',typ.encode()),(b'content-length',str(len(data)).encode())]});await send({'type':'http.response.body','body':data})
config=GateConfig(public_origin='https://wyw.ericmo.top',client_file=ROOT/'.local/security-client.json',title='文言星图',mark='文',description='从原文出发，连接不同篇目的知识。')
app=EmailAuthMiddleware(business,config=config)
