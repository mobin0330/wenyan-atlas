"""Author the transparent prototype corpus. No textbook membership is inferred."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D={k:[] for k in ('sources','works','sentences','lexemes','senses','occurrences','questions','textbook_editions','volumes','memberships')}
D['version']='sample-0.1.0'
for id,title,url,revision in [
 ('mengzi','《孟子·告子上》第九章','https://zh.wikisource.org/w/index.php?title=孟子/告子上&oldid=2637004','oldid=2637004'),
 ('loushi','《陋室铭》','https://zh.wikisource.org/w/index.php?title=陋室銘&oldid=11122639','oldid=11122639'),
 ('ailian','《爱莲说》','https://zh.wikisource.org/wiki/愛蓮說','2026-11-04 查阅；后续人审应固定修订号')]:
 D['sources'].append(dict(id=id,title=title,url=url,revision=revision,rights='古代原作公有领域；维基文库整理层按 CC BY-SA 4.0 署名并保留链接',note='仅取原文，自行简化字与分句；未复制现代教材注释。释义为本项目待审核稿。'))
texts=[
 ('xueyi','学弈','《孟子》','先秦','比较两位学习者的注意力与结果。节选自《告子上》，标题为常用选段名，未确认教材归属。','mengzi',[
 ('弈秋，通国之善弈者也。','弈秋，通國之善弈者也。','弈秋是全国擅长下棋的人。'),
 ('使弈秋诲二人弈：其一人专心致志，惟弈秋之为听；一人虽听之，一心以为有鸿鹄将至，思援弓缴而射之。','使弈秋誨二人弈：其一人專心致志，惟弈秋之為聽；一人雖聽之，一心以為有鴻鵠將至，思援弓繳而射之。','两人同学下棋，一人专心，一人想着射鸟。原典用“惟”，不替换为未经核对的教材字形。'),
 ('虽与之俱学，弗若之矣。','雖與之俱學，弗若之矣。','虽然一起学习，结果却不如那位专心的人。'),
 ('为是其智弗若与？曰：非然也。','為是其智弗若與？曰：非然也。','这是因为他的智力不如对方吗？回答：不是这样。')]),
 ('loushi','陋室铭','刘禹锡','唐','借居室陈设和交往说明志趣。这里以原典节选呈现，不代替教材全文。','loushi',[
 ('山不在高，有仙则名。水不在深，有龙则灵。','山不在高，有仙則名。水不在深，有龍則靈。','开篇用山水作比。'),
 ('斯是陋室，惟吾德馨。','斯是陋室，惟吾德馨。','居所虽简陋，重在居住者的品德。'),
 ('无丝竹之乱耳，无案牍之劳形。','無絲竹之亂耳，無案牘之勞形。','以两组主谓结构写没有喧闹声和公文带来的烦扰。'),
 ('孔子云：何陋之有？','孔子云：何陋之有？','“何陋”移到“有”前面；具体语法标签留待教师复核。')]),
 ('ailian','爱莲说','周敦颐','北宋','以莲的生长与姿态寄托志趣。这里以原典节选呈现，不代替教材全文。','ailian',[
 ('水陆草木之花，可爱者甚蕃。','水陸草木之花，可愛者甚蕃。','水上陆地上的花，值得喜爱的很多。'),
 ('予独爱莲之出淤泥而不染，濯清涟而不妖。','予獨愛蓮之出淤泥而不染，濯清漣而不妖。','写莲的生长环境和姿态，用来表达作者的欣赏。'),
 ('予谓菊，花之隐逸者也；牡丹，花之富贵者也；莲，花之君子者也。','予謂菊，花之隱逸者也；牡丹，花之富貴者也；蓮，花之君子者也。','用不同的人格类型比喻三种花。')])]
for wid,title,author,era,intro,src,rows in texts:
 D['works'].append(dict(id=wid,title=title,author=author,era=era,intro=intro,source_id=src,status='pending',version=D['version']))
 for i,(text,original,explanation) in enumerate(rows):D['sentences'].append(dict(id=f'{wid}-{i+1}',work_id=wid,position=i+1,text=text,source_text=original,explanation=explanation,status='pending'))
for id,text in [('zhi','之'),('er','而'),('qi','其')]:D['lexemes'].append(dict(id=id,text=text))
senses=[
 ('zhi-pronoun','zhi','指代人或事物','在句中代替前文提到的人、物或事情，具体指什么必须回看语境。','代词','zhī','mengzi','“听之”“射之”“与之”里的指代对象不同，不能只背“他”。'),
 ('zhi-of','zhi','连接修饰关系','连接修饰成分与中心词，有些语境可以用现代汉语“的”帮助理解。','结构助词','zhī','ailian','“通国之善弈者”“草木之花”可对照；不能把所有“之”都译作“的”。'),
 ('zhi-clause','zhi','用于主谓之间','把主谓结构连成句中的一个成分，传统教学常称“取消句子独立性”，一般不单独译出。','助词','zhī','loushi','标签为本项目候选解释，尚未对照目标版教材或教师审核。'),
 ('zhi-front','zhi','宾语前置标志','“何陋之有”可按“有何陋”理解，这里的“之”不指代具体人物。','句式标志','zhī','loushi','只标注本句，不自动推广到“菊之爱”等有不同分析的例子。'),
 ('er-turn','er','表示转折','前后意思有转折，可尝试用“却”理解，再检查是否符合句意。','连词','ér','ailian','只解释本处语境。'),
 ('er-link','er','连接动作','把前后动作连接起来，先理解动作关系，再决定现代汉语表达。','连词','ér','mengzi','不强行给所有动作关系加统一“承接”结论。'),
 ('qi-pronoun','qi','表示其中或他的','结合所在短语判断指代范围；“其一人”是其中一人。','代词','qí','mengzi','当前只纳入“其一人”的示例。')]
for id,l,label,definition,grammar,reading,src,note in senses:D['senses'].append(dict(id=id,lexeme_id=l,label=label,definition=definition,grammar=grammar,reading=reading,source_id=src,note=note,status='pending'))
occ=[('xueyi-1','之',0,'zhi-of','修饰关系：通国 → 善弈者。'),('xueyi-2','之',1,'zhi-pronoun','“听之”指听弈秋讲授；须和“射之”的对象区分。'),('xueyi-2','之',2,'zhi-pronoun','“射之”指向前文鸿鹄。'),('xueyi-3','之',0,'zhi-pronoun','指那位专心学习的人。'),('xueyi-3','之',1,'zhi-pronoun','仍指专心学习的人。'),('ailian-1','之',0,'zhi-of','修饰关系：草木 → 花。'),('ailian-3','之',0,'zhi-of','花 → 隐逸者。'),('ailian-2','之',0,'zhi-clause','莲 → 出淤泥而不染。'),('loushi-3','之',0,'zhi-clause','丝竹 → 乱耳。'),('loushi-3','之',1,'zhi-clause','案牍 → 劳形。'),('loushi-4','之',0,'zhi-front','原语序为“何陋之有”。'),('ailian-2','而',0,'er-turn','身处淤泥，却不被沾染。'),('ailian-2','而',1,'er-turn','洗濯却不显得妖艳。'),('xueyi-2','而',0,'er-link','拉弓和射鸟两个动作相连接。'),('xueyi-2','其',0,'qi-pronoun','“其一人”指两人中的一个人。')]
for i,(sid,word,n,sense,note) in enumerate(occ):
 sentence=next(s for s in D['sentences'] if s['id']==sid)['text']; positions=[j for j,c in enumerate(sentence) if c==word]; start=positions[n]; lex=next(l['id'] for l in D['lexemes'] if l['text']==word)
 D['occurrences'].append(dict(id=f'occ-{i+1}',sentence_id=sid,lexeme_id=lex,sense_id=sense,start=start,end=start+1,note=note,status='pending'))
qs=[('occ-2','“一人虽听之”中的“之”，应结合哪一项来理解？',['弈秋的讲授','鸿鹄','现代汉语“的”'],0,'先看“听”这个动作，再回看前文是谁在教授。'),('occ-3','“思援弓缴而射之”中的“之”指什么？',['弈秋','鸿鹄','学习下棋'],1,'回到前半句，找出这个人想象中将要到来的对象。'),('occ-6','“水陆草木之花”中的“之”与哪一种用法相近？',['通国之善弈者也','一人虽听之','思援弓缴而射之'],0,'观察它前后的词：是否在说“哪一类的什么”？'),('occ-8','“莲之出淤泥而不染”与哪句的结构较接近？',['无丝竹之乱耳','思援弓缴而射之','通国之善弈者也'],0,'比较“莲—出淤泥”与“丝竹—乱耳”是否分别构成主谓关系。'),('occ-11','“何陋之有”按通常语序可怎样理解？',['有何陋','何之有陋','有之何陋'],0,'先找到动词“有”，再找它询问的对象。'),('occ-12','“出淤泥而不染”中，“而”前后的意思是？',['转折','指代','修饰'],0,'前面说环境，后面说没有受到这种环境的影响。')]
for i,(oid,prompt,choices,answer,hint) in enumerate(qs):
 o=next(o for o in D['occurrences'] if o['id']==oid)
 D['questions'].append(dict(id=f'q-{i+1}',occurrence_id=oid,prompt=prompt,choices=choices,answer=answer,explanation=o['note'],hint=hint,status='pending',version=D['version']))
(ROOT/'data/sample.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
print('Sample authored:',len(D['works']),'works,',len(D['occurrences']),'occurrences; no approvals or textbook assignments.')
