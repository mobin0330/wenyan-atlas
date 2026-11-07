"""Deterministic knowledge and learning domain. No model or network calls."""
import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCOPES = {'小学': [1,2,3,4,5], '六年级': [6], '七年级': [7], '八年级': [8], '九年级': [9]}
TABLES = ('sources','works','sentences','lexemes','senses','occurrences','questions','textbook_editions','volumes','memberships')
REVIEWABLE = ('works','sentences','senses','occurrences','questions','textbook_editions','memberships')


def scopes(value):
    if not isinstance(value,list) or not value or any(not isinstance(x,str) or x not in SCOPES for x in value):
        raise ValueError('学习范围至少选择一项，且只能使用五个标准选项。')
    return list(dict.fromkeys(value))


class Atlas:
    def __init__(self,path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            for migration in sorted((ROOT/'migrations').glob('*.sql')):db.executescript(migration.read_text())
            db.executemany('INSERT OR IGNORE INTO coverage_slots(grade,semester) VALUES(?,?)',[(g,t) for g in range(1,10) for t in ('上','下')])

    def connect(self):
        db=sqlite3.connect(self.path,timeout=5)
        db.row_factory=sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA journal_mode=WAL')
        return db

    def rows(self,table):
        if table not in TABLES+('content_reviews','coverage_slots'):raise ValueError('不支持的数据表')
        with self.connect() as db:return [dict(r) for r in db.execute('SELECT * FROM '+table)]

    def import_file(self,path):
        raw=Path(path).read_bytes(); d=json.loads(raw); digest=hashlib.sha256(raw).hexdigest()
        if not isinstance(d.get('version'),str):raise ValueError('缺少数据版本')
        with self.connect() as db:
            if db.execute('SELECT 1 FROM imports WHERE digest=?',(digest,)).fetchone():return {'imported':False,'reason':'相同数据已导入'}
            # One transaction; never overwrite a reviewed entity or existing source silently.
            for table in TABLES:
                allowed={r['name'] for r in db.execute('PRAGMA table_info('+table+')')}
                for source_row in d.get(table,[]):
                    row=dict(source_row)
                    if set(row)!=allowed:raise ValueError(f'{table} 字段不完整或有未知字段')
                    if 'status' in row and row['status']!='pending':raise ValueError('导入只能创建待审核记录，不能导入审批结论')
                    if table=='questions':
                        if not isinstance(row['choices'],list) or len(row['choices'])<2 or not all(isinstance(c,str) for c in row['choices']) or type(row['answer']) is not int or not 0<=row['answer']<len(row['choices']):raise ValueError('题目答案无效')
                        row['choices']=json.dumps(row['choices'],ensure_ascii=False)
                    existing=db.execute('SELECT * FROM '+table+' WHERE id=?',(row['id'],)).fetchone()
                    if existing:
                        old=dict(existing); old.pop('status',None); new=dict(row); new.pop('status',None)
                        if old!=new:raise ValueError(f'{table}/{row["id"]} 已存在不同内容：请新增内容版本，禁止覆盖')
                        continue
                    keys=list(row)
                    db.execute('INSERT INTO '+table+'('+','.join(keys)+') VALUES('+','.join('?' for _ in keys)+')',[row[k] for k in keys])
            self.validate(db)
            db.execute('INSERT INTO imports(digest,version) VALUES(?,?)',(digest,d['version']))
        return {'imported':True,'version':d['version']}

    def validate(self,db=None):
        own=db is None; db=db or self.connect()
        try:
            if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('存在悬空引用')
            for r in db.execute('SELECT o.*,s.text,l.text AS word,se.lexeme_id AS sense_lexeme FROM occurrences o JOIN sentences s ON s.id=o.sentence_id JOIN lexemes l ON l.id=o.lexeme_id JOIN senses se ON se.id=o.sense_id'):
                if r['text'][r['start']:r['end']]!=r['word']:raise ValueError('原文偏移与字词不一致：'+r['id'])
                if r['sense_lexeme']!=r['lexeme_id']:raise ValueError('义项不属于此字词：'+r['id'])
            overlaps=db.execute('SELECT a.id FROM occurrences a JOIN occurrences b ON a.sentence_id=b.sentence_id AND a.id<b.id AND a.start<b.end AND b.start<a.end').fetchall()
            if overlaps:raise ValueError('字词出现位置重叠')
            return {'valid':True,'foreign_keys':'ok','offsets':'ok','sense_links':'ok'}
        finally:
            if own:db.close()

    def review(self,table,id,status,reviewer,evidence):
        if table not in REVIEWABLE or status not in ('approved','disputed','retired','pending'):raise ValueError('非法审核操作')
        if not reviewer.strip() or len(evidence.strip())<10:raise ValueError('必须提供审核人和至少十个字符的依据/修改说明')
        with self.connect() as db:
            r=db.execute('SELECT status FROM '+table+' WHERE id=?',(id,)).fetchone()
            if not r:raise ValueError('记录不存在')
            self.validate(db)
            db.execute('UPDATE '+table+' SET status=? WHERE id=?',(status,id))
            db.execute('INSERT INTO content_reviews(entity_type,entity_id,previous_status,new_status,reviewer,evidence) VALUES(?,?,?,?,?,?)',(table,id,r['status'],status,reviewer.strip(),evidence.strip()))
        return {'ok':True}

    def corpus(self,selected=None,sample=False):
        selected=scopes(selected or ['小学']); grades=sum((SCOPES[x] for x in selected),[])
        d={t:self.rows(t) for t in TABLES}
        if not sample:
            ed={x['id'] for x in d['textbook_editions'] if x['status']=='approved'}
            vols={x['id'] for x in d['volumes'] if x['edition_id'] in ed and x['grade'] in grades}
            works={x['work_id'] for x in d['memberships'] if x['status']=='approved' and x['volume_id'] in vols and x['category']=='课内文言文'}
            d['works']=[w for w in d['works'] if w['status']=='approved' and w['id'] in works]
            wids={w['id'] for w in d['works']}
            d['sentences']=[s for s in d['sentences'] if s['status']=='approved' and s['work_id'] in wids]
            d['senses']=[s for s in d['senses'] if s['status']=='approved']
            sids={s['id'] for s in d['sentences']}; senses={s['id'] for s in d['senses']}
            d['occurrences']=[o for o in d['occurrences'] if o['status']=='approved' and o['sentence_id'] in sids and o['sense_id'] in senses]
        lids={o['lexeme_id'] for o in d['occurrences']}; senses={o['sense_id'] for o in d['occurrences']}
        d['lexemes']=[l for l in d['lexemes'] if l['id'] in lids]
        d['senses']=[s for s in d['senses'] if s['id'] in senses]
        oids={o['id'] for o in d['occurrences']}
        d['questions']=[q for q in d['questions'] if q['occurrence_id'] in oids and (sample or q['status']=='approved')]
        for q in d['questions']:
            q['choices']=json.loads(q['choices']); q.pop('answer'); q.pop('explanation')
        source_ids={w['source_id'] for w in d['works']} | {s['source_id'] for s in d['senses']}
        d['sources']=[s for s in d['sources'] if s['id'] in source_ids]
        # Catalog metadata also has a publication boundary; candidate associations never leak as facts.
        approved_ed={x['id'] for x in d['textbook_editions'] if x['status']=='approved'}
        d['textbook_editions']=[x for x in d['textbook_editions'] if x['id'] in approved_ed]
        d['volumes']=[x for x in d['volumes'] if x['edition_id'] in approved_ed]
        vids={v['id'] for v in d['volumes']}; wids={w['id'] for w in d['works']}
        d['memberships']=[m for m in d['memberships'] if m['status']=='approved' and m['volume_id'] in vids and m['work_id'] in wids]
        return d

    def graph(self,lexeme,selected=None,sample=False,sense=None):
        d=self.corpus(selected,sample)
        l=next((x for x in d['lexemes'] if x['id']==lexeme),None)
        if not l:return {'nodes':[],'edges':[],'has_more':False}
        senses=[s for s in d['senses'] if s['lexeme_id']==lexeme and (not sense or s['id']==sense)][:8]
        ids={s['id'] for s in senses}; all_occ=[o for o in d['occurrences'] if o['sense_id'] in ids]
        sentence_works={s['id']:s['work_id'] for s in d['sentences']}; curriculum_works={w['id'] for w in d['works'] if w.get('curriculum')}
        all_occ.sort(key=lambda o:0 if sentence_works[o['sentence_id']] in curriculum_works else 1)
        occ=all_occ[:12]
        sentences={s['id']:s for s in d['sentences']}; works={w['id']:w for w in d['works']}
        nodes=[{'id':'l:'+l['id'],'kind':'lexeme','label':l['text'],'entity':l['id']}]; edges=[]
        for s in senses:
            nodes.append({'id':'s:'+s['id'],'kind':'sense','label':s['label'],'entity':s['id']})
            edges.append({'from':'l:'+l['id'],'to':'s:'+s['id'],'label':'具有用法'})
        for o in occ:
            sentence=sentences[o['sentence_id']]; work=works[sentence['work_id']]
            nodes.append({'id':'o:'+o['id'],'kind':'occurrence','label':sentence['text'],'entity':o['id'],'work':work['title'],'work_id':work['id']})
            edges.append({'from':'s:'+o['sense_id'],'to':'o:'+o['id'],'label':'本处采用'})
        return {'nodes':nodes,'edges':edges,'has_more':len(all_occ)>12,'total_occurrences':len(all_occ),'limit':21}

    def answer(self,qid,choice,hinted=False,selected=None,sample=False,profile=None,now=None):
        if type(choice) is not int or type(hinted) is not bool:raise ValueError('答案格式不正确')
        public=self.corpus(selected,sample)
        q=next((q for q in public['questions'] if q['id']==qid),None)
        if not q or not 0<=choice<len(q['choices']):raise ValueError('题目不可用或答案越界')
        with self.connect() as db:
            full=dict(db.execute('SELECT * FROM questions WHERE id=?',(qid,)).fetchone())
            o=db.execute('SELECT o.sense_id,s.work_id FROM occurrences o JOIN sentences s ON s.id=o.sentence_id WHERE o.id=?',(q['occurrence_id'],)).fetchone()
            correct=choice==full['answer']; saved=False
            if profile:
                now=now or datetime.now(timezone.utc); day=now.date().isoformat()
                cur=db.execute('INSERT OR IGNORE INTO learning_records(profile,kind,work_id,sense_id,question_id,correct,hinted,created_at,day) VALUES(?,?,?,?,?,?,?,?,?)',(profile,'discrimination',o['work_id'],o['sense_id'],qid,int(correct),int(hinted),now.isoformat(),day))
                saved=cur.rowcount>0
        return {'correct':correct,'answer':full['answer'],'explanation':full['explanation'],'hint':full['hint'],'sense_id':o['sense_id'],'work_id':o['work_id'],'recorded':saved,'diagnosis':None if correct else '可能混淆了本句用法；这只是待验证的判断，请对照原句后换一道题再试。'}

    def records(self,profile):
        with self.connect() as db:return [dict(r) for r in db.execute('SELECT kind,work_id,sense_id,question_id,correct,hinted,created_at,day FROM learning_records WHERE profile=? ORDER BY created_at DESC',(profile,))]

    def read(self,profile,wid,selected,sample=False):
        if not any(w['id']==wid for w in self.corpus(selected,sample)['works']):raise ValueError('课文未发布')
        now=datetime.now(timezone.utc)
        with self.connect() as db:db.execute('INSERT INTO learning_records(profile,kind,work_id,created_at,day) VALUES(?,?,?,?,?)',(profile,'read',wid,now.isoformat(),now.date().isoformat()))

    def preferences(self,profile,selected=None):
        with self.connect() as db:
            if selected is not None:
                selected=scopes(selected)
                db.execute('INSERT INTO preferences(profile,scopes) VALUES(?,?) ON CONFLICT(profile) DO UPDATE SET scopes=excluded.scopes',(profile,json.dumps(selected,ensure_ascii=False)))
            r=db.execute('SELECT scopes FROM preferences WHERE profile=?',(profile,)).fetchone()
        return json.loads(r['scopes']) if r else ['小学']

    def coverage(self):
        with self.connect() as db:
            verified=db.execute("SELECT COUNT(DISTINCT v.id) FROM volumes v JOIN textbook_editions e ON e.id=v.edition_id JOIN memberships m ON m.volume_id=v.id WHERE e.status='approved' AND m.status='approved'").fetchone()[0]
        return {'target_slots':18,'volumes_with_verified_membership':verified,'textbook_work_total':None,'coverage_percent':None,'slots':self.rows('coverage_slots'),'note':'篇目总数未核验，不能计算覆盖率；原典样例不计入教材。'}
