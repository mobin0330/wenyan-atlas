import tempfile,unittest
from pathlib import Path
from atlas import Atlas,ROOT
from recitation import save,records
from curriculum import enrich,LINKS
from asgi_app import TrialAtlas
class RecitationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.a=Atlas(Path(self.tmp.name)/'test.sqlite');self.a.import_file(ROOT/'data/trial.json')
 def tearDown(self):self.tmp.cleanup()
 def payload(self):return {'work_id':'jie-zi','sentence_ids':['jie-zi-1'],'mode':'hidden','self_rating':'self_independent','reveals':0}
 def test_self_assessment_has_independent_storage_and_version(self):
  r=save(self.a,'p',self.payload(),['七年级'],True);self.assertFalse(r['verified']);self.assertEqual(len(records(self.a,'p')),1);self.assertTrue(records(self.a,'p')[0]['text_version']);self.assertEqual(self.a.records('p'),[])
 def test_other_work_sentence_is_rejected(self):
  p=self.payload();p['sentence_ids']=['lang-1']
  with self.assertRaises(ValueError):save(self.a,'p',p,['七年级'],True)
 def test_independent_cannot_include_reveal_or_visible_text(self):
  for override in [{'reveals':1},{'mode':'read'},{'mode':'keywords'}]:
   p={**self.payload(),**override}
   with self.assertRaises(ValueError):save(self.a,'p',p,['七年级'],True)
 def test_assistance_and_profile_isolation(self):
  p={**self.payload(),'reveals':2,'self_rating':'with_help'};save(self.a,'p',p,['七年级'],True);self.assertEqual(records(self.a,'p')[0]['reveals'],2);self.assertEqual(records(self.a,'other'),[])
 def test_empty_duplicate_invalid_scope_and_unpublished_rejected(self):
  for ids in [[],['jie-zi-1','jie-zi-1'],['bad']]:
   with self.assertRaises(ValueError):save(self.a,'p',{**self.payload(),'sentence_ids':ids},['七年级'],True)
  with self.assertRaises(ValueError):save(self.a,'p',self.payload(),['七年级'],False)
 def test_source_evidence_does_not_promote_candidates(self):
  d=enrich(self.a.corpus(['七年级'],True));w=next(w for w in d['works']if w['id']=='chen-tai');self.assertEqual(w['curriculum']['book']['grade'],7);self.assertEqual(w['status'],'pending');self.assertNotIn('si-ma',LINKS);self.assertIn('版权页',w['curriculum']['book']['edition'])
 def test_history_snapshot_detects_changed_text(self):
  save(self.a,'p',self.payload(),['七年级'],True);before=records(self.a,'p')[0];self.assertTrue(before['practice_id']);self.assertTrue(before['current_text_matches'])
  with self.a.connect()as db:db.execute("UPDATE sentences SET text=text||'改' WHERE id='jie-zi-1'")
  self.assertFalse(records(self.a,'p')[0]['current_text_matches'])
 def test_corrected_grade_link_is_in_seventh_not_sixth(self):
  a=TrialAtlas(self.a.path);six={w['id']for w in a.corpus(['六年级'],True)['works']};seven={w['id']for w in a.corpus(['七年级'],True)['works']}
  for wid in ['chen-tai','yong-xue','lunyu-12']:self.assertIn(wid,seven);self.assertNotIn(wid,six)
if __name__=='__main__':unittest.main()
