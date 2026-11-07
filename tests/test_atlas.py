import copy,json,tempfile,unittest
from datetime import datetime,timezone,timedelta
from pathlib import Path
from atlas import Atlas,ROOT,scopes

class AtlasTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.a=Atlas(self.root/'test.sqlite');self.a.import_file(ROOT/'data/sample.json')
 def tearDown(self):self.tmp.cleanup()
 def seed(self):return json.loads((ROOT/'data/sample.json').read_text())
 def write(self,d):
  p=self.root/'input.json';p.write_text(json.dumps(d,ensure_ascii=False));return p
 def publish_fixture(self):
  # Synthetic curriculum metadata exists ONLY in isolated tests, never in the product dataset.
  with self.a.connect() as db:
   for t in ('works','sentences','senses','occurrences','questions'):db.execute('UPDATE '+t+" SET status='approved'")
   db.execute("INSERT INTO textbook_editions VALUES('test-ed','TEST ONLY','5-4','TEST','TEST','mengzi','approved')")
   db.execute("INSERT INTO volumes VALUES('test-v','test-ed',6,'上')")
   db.execute("INSERT INTO memberships VALUES('test-m','test-v','xueyi','TEST','课内文言文','TEST','TEST ONLY','approved')")
 def test_idempotent_init_and_import(self):
  self.assertFalse(self.a.import_file(ROOT/'data/sample.json')['imported']);Atlas(self.a.path)
  self.assertEqual(len(self.a.rows('occurrences')),15)
 def test_offsets_and_foreign_keys(self):self.assertTrue(self.a.validate()['valid'])
 def test_pending_cannot_publish(self):
  d=self.a.corpus(['小学'],False);self.assertEqual(d['works'],[]);self.assertEqual(d['senses'],[]);self.assertEqual(d['questions'],[])
 def test_sample_is_not_curriculum(self):
  self.assertEqual(len(self.a.corpus(sample=True)['works']),3);self.assertEqual(self.a.rows('memberships'),[]);self.assertIsNone(self.a.coverage()['coverage_percent'])
 def test_scope_validation(self):
  for s in ([],['大学'],None,'小学',[1]):
   with self.assertRaises(ValueError):scopes(s)
  self.assertEqual(scopes(['小学','小学','六年级']),['小学','六年级'])
 def test_real_grade_filter_and_multiple_scopes(self):
  self.publish_fixture();self.assertEqual(self.a.corpus(['小学'])['works'],[])
  self.assertEqual(len(self.a.corpus(['六年级'])['works']),1)
  self.assertEqual(len(self.a.corpus(['小学','六年级'])['works']),1)
 def test_unreviewed_sentence_blocks_occurrence_and_question(self):
  self.publish_fixture()
  with self.a.connect() as db:db.execute("UPDATE sentences SET status='pending' WHERE id='xueyi-2'")
  d=self.a.corpus(['六年级']);self.assertFalse(any(o['sentence_id']=='xueyi-2' for o in d['occurrences']));self.assertFalse(any(q['id']=='q-1' for q in d['questions']))
 def test_graph_links_and_cap(self):
  g=self.a.graph('zhi',sample=True);ids={n['id'] for n in g['nodes']}
  self.assertLessEqual(len(g['nodes']),21)
  for e in g['edges']:self.assertIn(e['from'],ids);self.assertIn(e['to'],ids)
  self.assertEqual(self.a.graph('not-found',sample=True)['nodes'],[])
 def test_same_word_has_different_senses(self):
  d=self.a.corpus(sample=True);self.assertEqual(len([s for s in d['senses'] if s['lexeme_id']=='zhi']),4)
  self.assertEqual(len({o['sense_id'] for o in d['occurrences'] if o['lexeme_id']=='zhi'}),4)
 def test_answer_not_leaked_in_question_endpoint(self):
  for q in self.a.corpus(sample=True)['questions']:self.assertNotIn('answer',q);self.assertNotIn('explanation',q)
 def test_answers_and_candidate_diagnosis(self):
  self.assertTrue(self.a.answer('q-1',0,sample=True)['correct']);self.assertFalse(self.a.answer('q-1',1,sample=True)['correct']);self.assertIn('可能',self.a.answer('q-1',1,sample=True)['diagnosis'])
  with self.assertRaises(ValueError):self.a.answer('q-1',0,sample=False)
  for bad in (-1,100,True,'0'):
   with self.assertRaises(ValueError):self.a.answer('q-1',bad,sample=True)
 def test_first_answer_per_day_and_hint_separation(self):
  self.publish_fixture();day=datetime(2026,11,4,tzinfo=timezone.utc)
  a=self.a.answer('q-1',1,True,['六年级'],profile='p',now=day);b=self.a.answer('q-1',0,False,['六年级'],profile='p',now=day)
  self.assertTrue(a['recorded']);self.assertFalse(b['recorded']);self.assertEqual(self.a.records('p')[0]['correct'],0)
  self.a.answer('q-1',0,False,['六年级'],profile='p',now=day+timedelta(days=1));self.assertEqual(len(self.a.records('p')),2);self.assertEqual(self.a.records('other'),[])
 def test_scope_change_preserves_records(self):
  self.publish_fixture();self.a.answer('q-1',0,selected=['六年级'],profile='p');self.a.preferences('p',['小学']);self.assertEqual(len(self.a.records('p')),1)
 def test_read_not_mastery(self):
  self.publish_fixture();self.a.read('p','xueyi',['六年级']);r=self.a.records('p')[0];self.assertEqual(r['kind'],'read');self.assertIsNone(r['correct']);self.assertIsNone(r['sense_id'])
 def test_offset_failure_rolls_back_entire_import(self):
  d=self.seed();d['works'][0]['id']='bad';d['sentences'][0]['work_id']='bad';d['occurrences'][0]['start']=0;d['occurrences'][0]['end']=1
  before=len(self.a.rows('works'))
  with self.assertRaises(ValueError):self.a.import_file(self.write(d))
  self.assertEqual(len(self.a.rows('works')),before)
 def test_invalid_new_offset_is_detected(self):
  d=self.seed();d['occurrences'][0]['start']=0;d['occurrences'][0]['end']=1
  fresh=Atlas(self.root/'fresh.sqlite')
  with self.assertRaises(ValueError):fresh.import_file(self.write(d))
  self.assertEqual(fresh.rows('works'),[])
 def test_no_automatic_approval_import(self):
  d=self.seed();d['works'][0]['status']='approved'
  with self.assertRaises(ValueError):self.a.import_file(self.write(d))
 def test_review_audit_and_no_overwrite(self):
  self.a.review('senses','zhi-pronoun','approved','Test reviewer','这是测试审核依据，不代表正式内容审核。')
  self.assertEqual(len(self.a.rows('content_reviews')),1)
  self.a.import_file(ROOT/'data/sample.json');self.assertEqual(self.a.rows('senses')[0]['status'],'approved')
  d=self.seed();d['senses'][0]['definition']='different'
  with self.assertRaises(ValueError):self.a.import_file(self.write(d))
 def test_missing_review_evidence_rejected(self):
  with self.assertRaises(ValueError):self.a.review('works','xueyi','approved','','')
 def test_backup_restore(self):
  import sqlite3
  p=self.root/'copy.sqlite'
  with self.a.connect() as a,sqlite3.connect(p) as b:a.backup(b)
  self.assertEqual(len(Atlas(p).rows('occurrences')),15)

if __name__=='__main__':unittest.main()
