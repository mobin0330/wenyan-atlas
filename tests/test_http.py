import json,os,sys,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from unittest.mock import patch
from server import build_server
from atlas import ROOT

class HTTPTests(unittest.TestCase):
 def setUp(self):
  self.server=build_server(0);threading.Thread(target=self.server.serve_forever,daemon=True).start();self.url='http://127.0.0.1:'+str(self.server.server_port)
 def tearDown(self):self.server.shutdown();self.server.server_close();self.server.fixture_temp.cleanup()
 def get(self,path):
  with urllib.request.urlopen(self.url+path) as r:return r.status,json.load(r)
 def test_bootstrap_and_graph(self):
  _,d=self.get('/api/bootstrap');self.assertTrue(d['preview']);self.assertEqual(len(d['corpus']['works']),3)
  _,g=self.get('/api/graph?lexeme=zhi');self.assertLessEqual(len(g['nodes']),21)
 def test_formal_mode_does_not_leak_pending(self):self.assertEqual(self.get('/api/bootstrap?mode=published')[1]['corpus']['works'],[])
 def test_preview_cannot_use_private_db(self):
  with self.assertRaises(SystemExit):build_server(0,False,Path('/does/not/exist.sqlite'))
 def test_cannot_read_files(self):
  for path in ('/../PRODUCT.md','/data/sample.json','/.local/atlas.sqlite','/docs/DATA.md'):
   with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(self.url+path)
   self.assertEqual(e.exception.code,404)
 def test_post_answer(self):
  req=urllib.request.Request(self.url+'/api/attempt',data=json.dumps({'question_id':'q-1','choice':0}).encode(),headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(req) as r:self.assertTrue(json.load(r)['correct'])
  self.assertEqual(self.server.atlas.records('household'),[])
 def test_scope_error_and_missing_question(self):
  with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(self.url+'/api/bootstrap?scopes=invalid')
  self.assertEqual(e.exception.code,400)
 def test_rate_limit(self):
  import time
  self.server.requests.extend([time.monotonic()]*240)
  with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(self.url+'/api/health')
  self.assertEqual(e.exception.code,429)
 def test_private_missing_config_fail_closed(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(SystemExit):build_server(0,True)
 def test_actual_shared_sdk_rejects_unauthenticated_and_wrong_host(self):
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'ATLAS_ORIGIN':'https://atlas.example.test','ATLAS_CLIENT_FILE':tmp+'/missing.json'}):
   srv=build_server(0,True,Path(tmp)/'db.sqlite');threading.Thread(target=srv.serve_forever,daemon=True).start()
   try:
    url='http://127.0.0.1:'+str(srv.server_port)
    for host,code in [('wrong.test',403),('atlas.example.test',401)]:
     req=urllib.request.Request(url+'/api/bootstrap',headers={'Host':host,'X-Forwarded-Proto':'https'})
     with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(req)
     self.assertEqual(e.exception.code,code)
   finally:srv.shutdown();srv.server_close()

if __name__=='__main__':unittest.main()
