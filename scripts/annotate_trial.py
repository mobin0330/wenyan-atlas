"""Explicit context anchors, never auto-assign meanings to every matching character."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from atlas import ROOT
D=json.loads((ROOT/'data/trial.json').read_text())
# word, sense, definition, context anchors: explanations are original candidate drafts.
specs=[
('之','pronoun','指代前文的人、物或事情','代词','zhī',['取之，信然','击瓮破之','下车引之','孔子不能决也','见之，拊掌','然之','颔之','遣之','知之','渔人甚异之','具答之','以记之']),
('之','of','连接修饰关系，可用“的”辅助理解','结构助词','zhī',['夫君子之行','山川之美','先天下之忧','后天下之乐','醉翁之意','宴酣之乐','小大之狱','忠之属也','吾盾之坚','吾矛之利','以子之矛','子之盾','水陆草木之花']),
('而','turn','连接有转折意味的前后内容','连词','ér',['人不知而不愠','出淤泥而不染','可远观而不可亵玩','而钱不湿','而身为宋国笑','千里马常有，而伯乐不常有']),
('而','link','连接前后动作，结合原句判断动作关系','连词','ér',['结友而别','康肃笑而遣之','释担而立','折颈而死','余强饮三大白而别','学而时习之']),
('其','his','指代相关人物或事物，具体所指要回看前文','代词','qí',['誉其矛','其人弗能应','孔君平诣其父','见其发矢','以钱覆其口','问其姓氏','安陵君其许寡人']),
('以','using','用、凭借；说明工具、条件或依据','介词','yǐ',['以照书','以我酌油','徐以杓酌油','以钱覆其口','可以一战','可以为师矣']),
('以','think','认为；“以为”须连起来理解','动词','yǐ',['我以日始出','我以日初出','自以为大有所益']),
('为','become','成为、做；结合本句的宾语理解','动词','wéi',['可以为师矣']),
('为','passive','被，表示被动关系','被动用法','wéi',['为宋国笑']),
('去','leave','离开（古义），不是“到某地去”的方向词','动词','qù',['众皆弃去','未成，弃去','太丘舍去','意与日去','睨之久而不去','去国怀乡']),
('走','run','奔跑（古义）','动词','zǒu',['兔走触株','诸儿竞走取之']),
('善','good-at','擅长','动词','shàn',['陈康肃公善射','通国之善弈者也']),
('善','praise','好，表示赞许','感叹用法','shàn',['善哉乎鼓琴']),
('汤','hot-water','热水（古义）','名词','tāng',['及其日中如探汤']),
('绝','stop','停止、消失','动词','jué',['湖中人鸟声俱绝','哀转久绝','猿则百叫无绝']),
('绝','cut','断绝、截断','动词','jué',['伯牙破琴绝弦','沿溯阻绝']),
('绝','unique','独一无二，极','形容用法','jué',['天下独绝']),
('但','only','只、只是','副词','dàn',['但手熟尔','但当涉猎','但少闲人']),
('顾','look-back','回头看','动词','gù',['元方入门不顾']),
('许','about','表示约数','数量用法','xǔ',['一百许里']),
('名','famous','出名、闻名','动词','míng',['有仙则名']),
('属','category','类','名词','shǔ',['忠之属也','有良田美池桑竹之属']),
('属','entrust','嘱托（与“嘱”相关的用法）','动词','zhǔ',['属予作文以记之']),
('故','reason','缘故、原因','名词','gù',['问其故']),
('故','old','旧的知识或旧事','名词用法','gù',['温故而知新']),
('信','true','确实、的确','副词','xìn',['取之，信然']),
('信','trust','诚信、守信用','名词','xìn',['则是无信']),
('乃','then','于是、才','副词','nǎi',['蒙乃始就学','乃取一葫芦','父不在，乃呼儿出','去后乃至']),
('焉','where','哪里、怎么','疑问用法','yān',['湖中焉得更有此人']),
('若','like','像、如同','动词用法','ruò',['猛浪若奔','巍巍乎若太山','汤汤乎若流水']),
]
specs += [
('秋','occasion','时候，关键时刻','名词','qiū',['此诚危急存亡之秋也']),
('修','height','长，这里形容身高','形容用法','xiū',['邹忌修八尺有余']),
('许','place','地方、处所','名词用法','xǔ',['先生不知何许人也']),
('因','rely','凭借、趁着','介词','yīn',['未若柳絮因风起']),
('少女','youngest','小女儿；这里不能套用现代“年轻女子”','古今异义','shào nǚ',['炎帝之少女']),
('之','of-reading','连接修饰关系，可用“的”辅助理解','结构助词','zhī',['三到之中']),
('股','thigh','大腿','古今异义','gǔ',['屠自后断其股','尾搐入两股间']),
('洞','dig','打洞；本句名词用作动词','词类活用','dòng',['一狼洞其中']),
('道','tell','讲述、谈论','动词','dào',['国人道之']),
('之','pronoun-more','指代前文的人或事物','代词','zhī',['因往晓之','知之者不如好之者','心乐之','复投之','求之于上流','寒暑易节，始一反焉']),
('许','about-more','表示约数','数量用法','xǔ',['潭中鱼可百许头']),
('是','this','这、这个','指示代词','shì',['是非木杮']),
('且','almost','将近','副词','qiě',['年且九十']),
('患','misfortune','祸患、灾难','名词','huàn',['故患有所不辟也']),
('淫','mislead','使迷惑、使动摇','使动用法','yín',['富贵不能淫']),
('曾','increase','同“增”，增加','通假候选','zēng',['曾益其所不能']),
]
lex={x['text']:x['id'] for x in D['lexemes']};counter=1000
for word,key,definition,grammar,reading,anchors in specs:
 lid=lex.setdefault(word,'word-'+'-'.join(str(ord(c)) for c in word))
 if not any(x['id']==lid for x in D['lexemes']):D['lexemes'].append(dict(id=lid,text=word))
 sid=lid+'-trial-'+key; matches=[]
 for s in D['sentences']:
  if s['work_id'] in ('xueyi','loushi','ailian'):continue
  for anchor in anchors:
   start=s['text'].find(anchor)
   if start<0 or word not in anchor:continue
   p=start+anchor.index(word)
   if any(o['sentence_id']==s['id'] and o['start']==p for o in D['occurrences']):continue
   matches.append((s,p,anchor))
 if not matches:continue
 src=next(w['source_id'] for w in D['works'] if w['id']==matches[0][0]['work_id'])
 D['senses'].append(dict(id=sid,lexeme_id=lid,label=definition.split('（')[0].split('，')[0],definition=definition+'。请用所在句子验证，勿机械套用到同字的其他出现位置。',grammar=grammar,reading=reading,source_id=src,note='原创试用标注，待学科编辑复核；仅对列出的具体语境建立关系。',status='pending'))
 for s,p,anchor in matches:
  counter+=1;oid='trial-occ-'+str(counter);note='本处“'+word+'”：'+definition+'。语境：'+anchor
  D['occurrences'].append(dict(id=oid,sentence_id=s['id'],lexeme_id=lid,sense_id=sid,start=p,end=p+len(word),note=note,status='pending'))
  alternatives={'之':['到、往','用在主谓之间，不单独译出','指代前文的人或事物','连接修饰关系，可用“的”辅助理解'],'其':['表示推测的语气','表示反问的语气'],'而':['表示转折，相当于“却”','连接前后动作','表示修饰关系'],'以':['因为','用、凭借','认为','来，用来'],'为':['被','做、成为','为了'],'去':['离开','除掉','距离'],'走':['奔跑','步行','逃跑'],'善':['擅长','好，表示赞许','善良'],'汤':['热水','菜汤','商朝君主名'],'绝':['断绝','消失、停止','独一无二','越过'],'但':['只是','但是','只要'],'顾':['回头看','拜访','照顾'],'许':['表示约数','答应','赞同'],'名':['出名','姓名','命名'],'属':['类','嘱托','接连'],'故':['缘故','旧的知识或旧事','因此'],'信':['诚信','确实','书信'],'乃':['于是、才','竟然','是'],'焉':['哪里、怎么','兼有“于之”的意思','句末语气'],'若':['像','如果','你']}
  pool=alternatives.get(word,['同意','观察','拿走']);distractors=[x for x in pool if x not in definition and definition not in x][:2]
  while len(distractors)<2:distractors.append(['表示疑问语气','表示条件关系'][len(distractors)])
  choices=[definition,*distractors];answer=counter%3;choices=choices[-answer:]+choices[:-answer] if answer else choices
  D['questions'].append(dict(id='trial-q-'+str(counter),occurrence_id=oid,prompt='结合原句，这一处“'+word+'”怎样理解？',choices=choices,answer=answer,explanation=note,hint='先找到这个字前后的动作、人物或事物，再判断它连接或指代什么。',status='pending',version=D['version']))
# Canonical senses are shared across articles, including the first prototype units.
canonical={'zhi-trial-pronoun':'zhi-pronoun','zhi-trial-pronoun-more':'zhi-pronoun','zhi-trial-of':'zhi-of','zhi-trial-of-reading':'zhi-of','er-trial-turn':'er-turn','er-trial-link':'er-link','word-35768-trial-about-more':'word-35768-trial-about'}
for o in D['occurrences']:o['sense_id']=canonical.get(o['sense_id'],o['sense_id'])
D['senses']=[s for s in D['senses'] if s['id'] not in canonical]
# Remove lexemes with no occurrences from selectors.
used={o['lexeme_id'] for o in D['occurrences']};D['lexemes']=[l for l in D['lexemes'] if l['id'] in used]
(ROOT/'data/trial.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n');print('Trial:',len(D['works']),'works',len(D['senses']),'senses',len(D['occurrences']),'anchors',len(D['questions']),'questions')
