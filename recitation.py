"""Independent, self-assessed practice; never ASR scoring or mastery inference."""
import hashlib,json
from datetime import datetime,timezone

def save(atlas,profile,body,selected,sample):
    wid=body.get('work_id');mode=body.get('mode');rating=body.get('self_rating');reveals=body.get('reveals',0);ids=body.get('sentence_ids')
    d=atlas.corpus(selected,sample);w=next((w for w in d['works'] if w['id']==wid),None)
    if not w:raise ValueError('当前范围不可练习这篇课文')
    if mode not in ('read','keywords','hidden')or rating not in ('needs_practice','with_help','self_independent'):raise ValueError('练习状态无效')
    if type(reveals)is not int or not 0<=reveals<=10000:raise ValueError('揭示次数无效')
    available={s['id']:s for s in d['sentences']if s['work_id']==wid}
    if not isinstance(ids,list)or not ids or len(ids)>500 or any(not isinstance(i,str)or i not in available for i in ids)or len(ids)!=len(set(ids)):raise ValueError('请选择本篇有效且不重复的句段')
    if rating=='self_independent'and(mode!='hidden'or reveals):raise ValueError('独立自评需要遮住原文且未揭示提示；否则请选择借助提示完成')
    text='\n'.join(available[i]['text']for i in ids);now=datetime.now(timezone.utc).isoformat()
    with atlas.connect()as db:
        db.execute('INSERT INTO recitation_sessions(profile,work_id,sentence_ids,mode,self_rating,reveals,text_version,text_digest,created_at)VALUES(?,?,?,?,?,?,?,?,?)',(profile,wid,json.dumps(ids),mode,rating,reveals,w['version'],hashlib.sha256(text.encode()).hexdigest(),now))
    return {'ok':True,'self_rating':rating,'verified':False,'note':'已保存自主练习记录，未进行语音或背诵正确性检测'}

def records(atlas,profile):
    with atlas.connect()as db:
        texts={r['id']:r['text']for r in db.execute('SELECT id,text FROM sentences')}
        result=[]
        for r in db.execute('SELECT id AS practice_id,work_id,sentence_ids,mode,self_rating,reveals,text_version,text_digest,created_at FROM recitation_sessions WHERE profile=? ORDER BY created_at DESC LIMIT 100',(profile,)):
            item=dict(r);ids=json.loads(item['sentence_ids']);digest=hashlib.sha256('\n'.join(texts.get(i,'')for i in ids).encode()).hexdigest()
            item['sentence_ids']=ids;item['current_text_matches']=all(i in texts for i in ids)and digest==item.pop('text_digest');result.append(item)
        return result
