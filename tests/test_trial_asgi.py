"""Exercise private trial routing with SDK gate; only the gateway is a test fake."""
import asyncio,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import asgi_app as site
from shared_email_auth.asgi import EmailAuthMiddleware
from atlas import ROOT
class FakeGateway:
 def validate(self,binding,token):return binding=='b'*32 and token=='t'*32
class TrialTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.a=site.TrialAtlas(Path(self.tmp.name)/'test.sqlite');self.a.import_file(ROOT/'data/trial.json');self.patch=patch.object(site,'atlas',self.a);self.patch.start();self.app=EmailAuthMiddleware(site.business,site.config,gateway=FakeGateway())
 def tearDown(self):self.patch.stop();self.tmp.cleanup()
 def request(self,path,query='',body=None,auth=True):
  async def run():
   hs=[(b'host',b'wyw.ericmo.top'),(b'x-forwarded-proto',b'https')]
   if auth:hs.append((b'cookie',('email_binding='+'b'*32+'; email_session='+'t'*32).encode()))
   raw=json.dumps(body).encode()if body is not None else b''
   if body is not None:hs.extend([(b'origin',b'https://wyw.ericmo.top'),(b'x-ncg-request',b'1'),(b'content-type',b'application/json'),(b'content-length',str(len(raw)).encode())])
   scope={'type':'http','method':'GET'if body is None else 'POST','path':path,'query_string':query.encode(),'headers':hs,'client':('127.0.0.1',1234)};msgs=[]
   async def receive():return {'type':'http.request','body':raw,'more_body':False}
   async def send(m):msgs.append(m)
   await self.app(scope,receive,send);return msgs[0]['status'],json.loads(msgs[-1]['body'])
  return asyncio.run(run())
 def test_all_five_scopes_have_units_and_knowledge(self):
  from urllib.parse import urlencode
  for scope in ['小学','六年级','七年级','八年级','九年级']:
   status,d=self.request('/api/bootstrap',urlencode({'mode':'trial','scopes':scope}));self.assertEqual(status,200);self.assertGreater(len(d['corpus']['works']),0);self.assertGreater(len(d['corpus']['occurrences']),0)
 def test_private_unauthed_api_denied(self):self.assertEqual(self.request('/api/bootstrap',auth=False)[0],401)
 def test_pending_not_in_formal(self):self.assertEqual(self.request('/api/bootstrap','mode=published')[1]['corpus']['works'],[])
 def test_trial_attempt_is_persisted_not_browsing_mastery(self):
  q=self.a.corpus(['小学'],True)['questions'][0];full=next(x for x in self.a.rows('questions')if x['id']==q['id']);status,d=self.request('/api/attempt','mode=trial',{'question_id':q['id'],'choice':full['answer'],'hinted':False});self.assertEqual(status,200);self.assertTrue(d['recorded']);self.assertEqual(len(self.request('/api/records')[1]['records']),1)
if __name__=='__main__':unittest.main()
