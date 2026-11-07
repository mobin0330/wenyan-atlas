"""Build auditable full-range research artifacts, without publishing candidate knowledge.
Uses cached public metadata/text. Source scans/transcripts remain under .local only.
"""
import csv,hashlib,json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';CACHE=ROOT/'.local/textbook-research';MIRRORS=CACHE/'mirrors'
NUM={'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
COPY={(1,'上'):'91242993',(1,'下'):'91242995',(2,'上'):'91242999',(2,'下'):'91243001',(3,'上'):'91242997',(3,'下'):'91242998',(4,'上'):'91243004',(4,'下'):'91243005',(5,'上'):'91243002',(5,'下'):'91243003',(6,'上'):'91248583',(6,'下'):'91248584',(7,'上'):'91248576',(7,'下'):'91248577',(8,'上'):'91244304',(8,'下'):'91248573',(9,'上'):'91244302',(9,'下'):'91248575'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def target_policy():
 path=DATA/'textbook-decisions.json'
 if not path.exists():return None
 decision=json.loads(path.read_text())
 if decision.get('status')!='confirmed':return None
 return {'id':decision['target_policy'],'label':decision['target_policy_label'],'confirmed_at':decision['confirmed_at'],'school_copy_selection_required':False,'notice':'目标原则已确定；具体出版版次与来源仍须核实，不代表正文或词义已审核。'}

def apply_target_policy(register):
 policy=target_policy()
 if policy is None:return register
 register['target_policy']=policy
 for book in register['books']:
  book['target_policy']=policy['id']
  book.setdefault('target_edition_verified',False)
  book['edition_notice']='采用最新正式出版修订版；具体版次与资料同版性仍待来源核实，不要求用户确认学校印次。'
  book['remaining']=[x.replace('确认版权版次和学校使用印次','核实最新正式修订版的版权版次及来源同版性') for x in book['remaining']]
 return register

def normal(s):return re.sub(r'[^\u4e00-\u9fff]','',s)
def head_pattern(title):
 # Printed superscript footnote letters can split title characters in OCR.
 return ''.join(re.escape(c)+r'[a-z《》〈〉，,·]?'for c in normal(title))
END_TARGET={
 '司马光':'掌声','守株待兔':'陶罐和铁罐','精卫填海':'普罗米修斯','王戎不取道旁李':'西门豹治邺',
 '囊萤夜读':'小英雄雨来','铁杵成针':'小英雄雨来','古人谈读书':'忆读书','自相矛盾':'田忌赛马','杨氏之子':'手指',
 '两小儿辩日':'写作','曹冲称象':'写作','学弈':'写作','关尹子教射':'写作',
 '咏雪':'阅读综合实践','陈太丘与友期行':'阅读综合实践','论语十二章':'阅读综合实践','诫子书':'阅读综合实践','狼':'任务二','穿井得一人':'阅读综合实践','杞人忧天':'阅读综合实践',
 '孙权劝学':'阅读综合实践','卖油翁':'阅读综合实践','陋室铭':'阅读综合实践','爱莲说':'阅读综合实践','活板':'任务二',
 '三峡':'短文二篇','答谢中书书':'与朱元思书','记承天寺夜游':'与朱元思书','与朱元思书':'唐诗五首',
 '得道多助，失道寡助':'愚公移山','富贵不能淫':'愚公移山','生于忧患，死于安乐':'愚公移山','愚公移山':'周亚夫军细柳','周亚夫军细柳':'诗词五首',
 '桃花源记':'小石潭记','小石潭记':'核舟记','核舟记':'诗经二首','北冥有鱼':'礼记二则','庄子与惠子游于濠梁之上':'礼记二则','虽有嘉肴':'马说','大道之行也':'马说','马说':'唐诗三首',
 '岳阳楼记':'醉翁亭记','醉翁亭记':'湖心亭看雪','湖心亭看雪':'诗词三首','鱼我所欲也':'唐雎不辱使命','唐雎不辱使命':'送东阳马生序','送东阳马生序':'词四首',
 '曹刿论战':'邹忌讽齐王纳谏','邹忌讽齐王纳谏':'陈涉世家','陈涉世家':'出师表','出师表':'诗词曲五首'}
def locate_section(text,title):
 text=re.sub('[ \t\u3000]','',text)
 pattern=head_pattern(title)
 hits=[m for m in re.finditer(pattern+r'(?:[①-⑳]|\n)',text)if m.start()>5000]
 if not hits:return None
 pos=hits[0].start();end=min(len(text),pos+14000)
 endtitle=END_TARGET[title];endpattern=head_pattern(endtitle)
 stop=re.search(endpattern+r'(?:[①-⑳（(]|\n)',text[pos+len(normal(title))+5:])
 if stop:end=min(end,pos+len(normal(title))+5+stop.start())
 return text[pos:end]
def extract_heads(section):
 if section is None:return []
 return list(dict.fromkeys(re.sub(r'[（(][^）)]*[）)]','',x) for x in re.findall(r'〔([^〕\n]{1,24})〕',section)))
def main():
 catalog=json.loads((ROOT/'.local/source-cache/pep-official-catalog.json').read_text())
 official=[b for b in catalog if b['xk']=='语文'and b.get('xdtype')=='义务教育（五四学制）'and b.get('sydx')=='学生'];assert len(official)==18
 directories=json.loads((DATA/'textbook-directory-observations.json').read_text())['observations'];assert len(directories)==18
 trial=json.loads((DATA/'trial.json').read_text());works={normal(w['title']):w for w in trial['works']}
 sentences={s['id']:s for s in trial['sentences']};occurrences=Counter(sentences[o['sentence_id']]['work_id']for o in trial['occurrences'])
 rows=list(csv.DictReader((DATA/'textbook-prose-observations.tsv').open(),delimiter='\t'));prose=[]
 for i,row in enumerate(rows):
  row['grade']=int(row['grade']);row['printed_page']=int(row.pop('page'));copy=row['copy'];textpath=MIRRORS/f'{copy}.txt';raw=MIRRORS/f'{copy}.html';text=textpath.read_text();assert text
  section=locate_section(text,row['title']);heads=extract_heads(section);w=works.get(normal(row['title']))
  if row['title']=='论语十二章':w=next((w for w in trial['works']if '论语' in w['title']),None)
  recitation=[]
  if section:
   for line in section.splitlines():
    if any(k in line for k in ['背诵','默写','熟读','朗读']):
     # Store task category only; never republish modern instructions verbatim.
     if '背诵'in line:recitation.append('背诵要求线索')
     if '默写'in line:recitation.append('默写要求线索')
     if '熟读'in line:recitation.append('熟读要求线索')
     if '朗读'in line:recitation.append('朗读要求线索')
  prose.append({**row,'id':f'prose-observation-{i+1:02}','source_url':f'https://www.yeyulingfeng.com/wendang/{copy}.html','source_sha256':digest(raw),'source_kind':'third_party_textbook_transcript','membership_status':'observed_in_named_copy','school_current_edition_confirmed':False,'page_notice':'合篇起页，不冒充子篇精确页码'if row['page_scope']=='合篇起页'else'所见电子本目录印刷页；仍需图像交叉核对','body_heading_located':section is not None,'note_headwords_candidates':heads,'note_headword_status':'OCR提取候选，合篇注释尚未分配到具体子篇；未完成逐句定位与教材图像校准','learning_requirement_clues':list(dict.fromkeys(recitation)),'learning_requirement_status':'篇内线索，未核清具体对象和范围；不自动标记必背/必默','existing_trial_work_id':w['id']if w else None,'existing_trial_occurrences':occurrences[w['id']]if w else 0,'knowledge_status':'未完成教材义项与出现实例审核'})
 books=[]
 for b in official:
  g=NUM[b['nj'][0]];semester=b['cc'][0];key=COPY[(g,semester)];directory=next(d for d in directories if d['grade']==g and d['semester']==semester);proses=[r for r in prose if r['grade']==g and r['semester']==semester];raw=MIRRORS/f'{key}.html';txt=MIRRORS/f'{key}.txt'
  books.append({'id':f'pep54-{g}{"a"if semester=="上"else"b"}-registry','grade':g,'semester':semester,'title':b['title'],'publisher':'人民教育出版社','system':'五四学制','official_catalog_url':'https://jc.pep.com.cn/','official_reader_url':b['pdfurl'],'official_catalog_key':b['id'],'official_metadata_status':'publisher_catalog_observed_in_normal_browser','copyright_edition_date':None,'edition_notice':'官方在线目录当前列项已确认；不从网址编码推断版权版次/印次。学校实用印次未确认。','school_current_edition_confirmed':False,'directory_observation':directory,'additional_directory_observations':[d for d in json.loads((DATA/'textbook-new-directory-observations.json').read_text())['observations']if d['grade']==g and d['semester']==semester],'observed_textbook_copy':{'url':f'https://www.yeyulingfeng.com/wendang/{key}.html','source_kind':'third_party_textbook_transcript','sha256':digest(raw),'text_chars':len(txt.read_text()),'edition_relation':'所见版本；与官方当前电子本的逐页同版核对未完成','public_distribution_authorized':False},'classical_prose_observation_ids':[r['id']for r in proses],'classical_prose_status':'所见版本发现文言散文'if proses else'所见目录未发现独立文言散文；尚不能宣称当前版本核验无篇目','remaining':['确认版权版次和学校使用印次','核对当前电子本完整目录','校准古代正文选段、字形、标点','按出现实例审核实词/虚词义项、读音与文言现象','核对背诵和默写对象及范围']})
 books.sort(key=lambda b:(b['grade'],b['semester']=='下'))
 notices=[{'type':'substantive_directory_conflict','books':['六上','六下'],'detail':'第三方历史目录六上列伯牙鼓琴、书戴嵩画牛，六下列学弈、两小儿辩日；所见修订本六上改为两小儿辩日、曹冲称象，六下为学弈、关尹子教射。必须保留各自出处，不能融合成同一版。'}, {'type':'version_conflict','books':['四上','五上','八上','八下'],'detail':'另有新版目录证据，课号/页码和部分现代文发生变化；旧版观察保留，不覆盖为当前版。'}, {'type':'source_quality','books':['七下'],'detail':'第三方文字目录夹有重复旧课名；已取得官方目录第5–7阅读器页，可据图清理；不能整页盲信。'}, {'type':'classification','books':['二上','二下'],'detail':'曹冲称象、亡羊补牢等同题名的现代改写不能当作文言原文；六上曹冲称象须单独记录。'}, {'type':'scope','books':['全部'],'detail':'古诗词、古典白话小说、语文园地古语和课外拓展分别登记，不冒充独立课内文言散文。'}]
 summary={'target_books':18,'official_catalog_entries_found':len(books),'directory_candidate_books':len(directories),'directory_candidate_entries':sum(len(d['entries'])for d in directories),'textbook_transcript_copies_found':len(books),'classical_prose_observations':len(prose),'body_headings_located':sum(p['body_heading_located']for p in prose),'note_headword_candidates':sum(len(p['note_headwords_candidates'])for p in prose),'existing_trial_work_matches':sum(bool(p['existing_trial_work_id'])for p in prose),'school_current_editions_fully_verified':0,'fully_reviewed_lexical_occurrences':0,'full_curriculum_total_known':False}
 register={'checked_at':'2026-11-05','scope':'上海五四学制人教版语文：一至九年级上下册','official_catalog_snapshot_sha256':digest(ROOT/'.local/source-cache/pep-official-catalog.json'),'summary':summary,'notice':'这是全范围来源与内容工作台账，不是全量教材准确性或授权发布完成声明。候选目录与所见教材副本分开；不同版次不合并。','books':books,'risks':notices}
 apply_target_policy(register)
 (DATA/'textbook-register.json').write_text(json.dumps(register,ensure_ascii=False,indent=2))
 (DATA/'textbook-content-inventory.json').write_text(json.dumps({'checked_at':'2026-11-05','notice':register['notice'],'items':prose},ensure_ascii=False,indent=2))
 with (ROOT/'docs/TEXTBOOK-CONTENT-INVENTORY.csv').open('w',newline='',encoding='utf-8-sig')as f:
  writer=csv.writer(f);writer.writerow(['年级','册次','篇目','所见版本课号','所见版本印刷页','页码范围','教材文档来源','正文标题定位','候选注释词头数','现有试用文本','现有候选实例数','学校当前版已确认'])
  for p in prose:writer.writerow([p['grade'],p['semester'],p['title'],p['lesson'],p['printed_page'],p['page_scope'],p['source_url'],p['body_heading_located'],len(p['note_headwords_candidates']),p['existing_trial_work_id']or'未收录',p['existing_trial_occurrences'],'否'])
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
