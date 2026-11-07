import asyncio,json,unittest
from pathlib import Path
from atlas import ROOT
from curriculum import LINKS
import asgi_app
class TextbookResearchTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.register=json.loads((ROOT/'data/textbook-register.json').read_text());cls.content=json.loads((ROOT/'data/textbook-content-inventory.json').read_text())['items'];cls.requirements=json.loads((ROOT/'data/textbook-learning-requirements.json').read_text())['items']
 def test_all_eighteen_unique_target_slots_have_publisher_entries(self):
  books=self.register['books'];self.assertEqual({(b['grade'],b['semester'])for b in books},{(g,s)for g in range(1,10)for s in ['上','下']});self.assertEqual(len(books),18)
  for b in books:self.assertTrue(b['official_reader_url'].startswith('https://book.pep.com.cn/'));self.assertEqual(b['system'],'五四学制')
 def test_candidates_never_claim_current_school_or_teacher_review(self):
  for b in self.register['books']:self.assertFalse(b['school_current_edition_confirmed']);self.assertIsNone(b['copyright_edition_date'])
  for p in self.content:self.assertFalse(p['school_current_edition_confirmed']);self.assertNotEqual(p['membership_status'],'approved')
  self.assertNotIn('si-ma',LINKS);self.assertFalse(self.register['summary']['full_curriculum_total_known'])
 def test_content_and_requirement_foreign_keys_and_sources_match(self):
  inventory={p['id']:p for p in self.content};self.assertEqual(len(inventory),52);self.assertEqual(len(self.requirements),len(inventory))
  for r in self.requirements:
   p=inventory[r['inventory_id']];self.assertEqual(r['title'],p['title']);self.assertEqual(r['source_sha256'],p['source_sha256']);self.assertEqual(len(r['source_sha256']),64);self.assertFalse(r['teacher_reviewed'])
 def test_shared_lesson_does_not_inherit_another_work_recitation(self):
  by_title={r['title']:r for r in self.requirements}
  for title in ['曹冲称象','铁杵成针','学弈','关尹子教射']:self.assertFalse(any(t['type']=='recite'for t in by_title[title]['tasks']))
  for title in ['两小儿辩日','囊萤夜读']:self.assertTrue(any(t['type']=='recite'for t in by_title[title]['tasks']))
 def test_required_ranges_and_dictation_stay_distinct(self):
  by_title={r['title']:r for r in self.requirements};self.assertEqual(by_title['送东阳马生序']['tasks'][0]['range'],'前两段');self.assertEqual(by_title['富贵不能淫']['tasks'][0]['range'],'指定片段')
  self.assertEqual({t['type']for t in by_title['陋室铭']['tasks']},{'recite','dictation'})
 def test_all_body_titles_are_found_but_not_all_lexical_meanings_approved(self):
  self.assertTrue(all(p['body_heading_located']for p in self.content));self.assertEqual(self.register['summary']['fully_reviewed_lexical_occurrences'],0)
 def test_source_api_whitelist_and_handbook(self):
  async def query(path):
   sent=[]
   async def receive():return {'type':'http.request','body':b''}
   async def send(e):sent.append(e)
   await asgi_app.business({'type':'http','method':'GET','path':path,'query_string':b''},receive,send)
   return sent[0]['status'],sent[1]['body']
  code,body=asyncio.run(query('/api/textbooks'));self.assertEqual(code,200);self.assertEqual(json.loads(body)['summary']['target_books'],18)
  code,body=asyncio.run(query('/api/handbook/textbooks'));self.assertEqual(code,200);self.assertIn('52不是'.encode(),body)
  code,_=asyncio.run(query('/api/handbook/../../.local/security-client.json'));self.assertEqual(code,400)
if __name__=='__main__':unittest.main()
