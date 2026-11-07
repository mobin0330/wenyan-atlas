"""Build complete classical reading units, retaining pending editorial status.
Original public-domain prose only; no upstream modern translations or commentary.
"""
import json,re,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from opencc import OpenCC
from atlas import ROOT
cc=OpenCC('t2s');cache=ROOT/'.local/source-cache';D=json.loads((ROOT/'data/sample.json').read_text());D['version']='trial-0.2.0'
# A separate reading recommendation is never a claim about textbook membership.
reading=[]
def add(wid,title,author,era,text,source_url,scope,origin='原典整理'):
 sid='source-'+wid
 D['sources'].append(dict(id=sid,title=origin+' · '+title,url=source_url,revision='2026-11-05 / sha256:'+hashlib.sha256(text.encode()).hexdigest(),rights='古代原作公有领域；整理来源许可证及署名见 data/ATTRIBUTION.md',note='完整学习选文；自行简体化、分句。年级为试用推荐，不代替目标教材目录核验。释义与习题待人工审核。'))
 D['works'].append(dict(id=wid,title=title,author=author,era=era,intro='先通读选文，再点击重点字词，比较同词在其他文章里的用法。',source_id=sid,status='pending',version=D['version']))
 for n,m in enumerate(re.finditer(r'[^。！？]+[。！？]?[”」』]?',cc.convert(text)),1):
  t=m.group().strip()
  if t:D['sentences'].append(dict(id=f'{wid}-{n}',work_id=wid,position=n,text=t,source_text=t,explanation='',status='pending'))
 reading.append(dict(work_id=wid,scope=scope,classification='阅读推荐 / 教材归属待核',source=source_url))
G=json.loads((cache/'guwen.json').read_text());chosen={'曹劌論戰':('cao-gui','曹刿论战','九年级'),'鄒忌諷齊王納諫':('zou-ji','邹忌讽齐王纳谏','九年级'),'唐雎不辱使命 ':('tang-ju','唐雎不辱使命','九年级'),'前出師表':('chu-shi','出师表','九年级'),'桃花源記':('tao-hua','桃花源记','八年级'),'陋室銘':('lou-shi-full','陋室铭','七年级'),'雜說·馬說':('ma-shuo','马说','八年级'),'岳陽樓記':('yue-yang','岳阳楼记','九年级'),'醉翁亭記':('zui-weng','醉翁亭记','九年级'),'五柳先生傳':('wu-liu','五柳先生传','八年级')}
for v in G['content']:
 for w in v['content']:
  if w['chapter'] in chosen:
   wid,title,scope=chosen[w['chapter']];author=cc.convert(w.get('author','')).strip();add(wid,title,author,'依原典','\n'.join(w['paragraphs']),'https://github.com/chinese-poetry/chinese-poetry/blob/master/蒙学/guwenguanzhi.json',scope,'古文观止 / chinese-poetry (MIT)')
manual=[
('si-ma','司马光','《宋史》','元','群儿戏于庭，一儿登瓮，足跌没水中。众皆弃去，光持石击瓮破之，水迸，儿得活。','小学'),
('shou-zhu','守株待兔','《韩非子》','战国','宋人有耕者。田中有株。兔走触株，折颈而死。因释其耒而守株，冀复得兔。兔不可复得，而身为宋国笑。','小学'),
('wang-rong','王戎不取道旁李','《世说新语》','南朝宋','王戎七岁，尝与诸小儿游。看道边李树多子折枝，诸儿竞走取之，唯戎不动。人问之，答曰：“树在道边而多子，此必苦李。”取之，信然。','小学'),
('nang-ying','囊萤夜读','《晋书》','唐','胤恭勤不倦，博学多通。家贫不常得油，夏月则练囊盛数十萤火以照书，以夜继日焉。','小学'),
('tie-chu','铁杵成针','《方舆胜览》','南宋','磨针溪，在象耳山下。世传李太白读书山中，未成，弃去。过是溪，逢老媪方磨铁杵。问之，曰：“欲作针。”太白感其意，还卒业。','小学'),
('yang-shi','杨氏之子','《世说新语》','南朝宋','梁国杨氏子九岁，甚聪惠。孔君平诣其父，父不在，乃呼儿出。为设果，果有杨梅。孔指以示儿曰：“此是君家果。”儿应声答曰：“未闻孔雀是夫子家禽。”','小学'),
('mao-dun','自相矛盾','《韩非子》','战国','楚人有鬻盾与矛者，誉之曰：“吾盾之坚，物莫能陷也。”又誉其矛曰：“吾矛之利，于物无不陷也。”或曰：“以子之矛陷子之盾，何如？”其人弗能应也。夫不可陷之盾与无不陷之矛，不可同世而立。','小学'),
('bo-ya','伯牙鼓琴','《吕氏春秋》','战国','伯牙鼓琴，锺子期听之。方鼓琴而志在太山，锺子期曰：“善哉乎鼓琴，巍巍乎若太山。”少选之间而志在流水，锺子期又曰：“善哉乎鼓琴，汤汤乎若流水。”锺子期死，伯牙破琴绝弦，终身不复鼓琴，以为世无足复为鼓琴者。','六年级'),
('dai-song','书戴嵩画牛','苏轼','北宋','蜀中有杜处士，好书画，所宝以百数。有戴嵩《牛》一轴，尤所爱，锦囊玉轴，常以自随。一日曝书画，有一牧童见之，拊掌大笑，曰：“此画斗牛也！牛斗，力在角，尾搐入两股间，今乃掉尾而斗，谬矣！”处士笑而然之。古语有云：“耕当问奴，织当问婢。”不可改也。','六年级'),
('bian-ri','两小儿辩日','《列子》','依原典','孔子东游，见两小儿辩斗，问其故。一儿曰：“我以日始出时去人近，而日中时远也。”一儿曰：“我以日初出远，而日中时近也。”一儿曰：“日初出大如车盖，及日中则如盘盂，此不为远者小而近者大乎？”一儿曰：“日初出沧沧凉凉，及其日中如探汤，此不为近者热而远者凉乎？”孔子不能决也。两小儿笑曰：“孰为汝多知乎？”','六年级'),
('chen-tai','陈太丘与友期行','《世说新语》','南朝宋','陈太丘与友期行，期日中。过中不至，太丘舍去，去后乃至。元方时年七岁，门外戏。客问元方：“尊君在不？”答曰：“待君久不至，已去。”友人便怒曰：“非人哉！与人期行，相委而去。”元方曰：“君与家君期日中。日中不至，则是无信；对子骂父，则是无礼。”友人惭，下车引之。元方入门不顾。','六年级'),
('yong-xue','咏雪','《世说新语》','南朝宋','谢太傅寒雪日内集，与儿女讲论文义。俄而雪骤，公欣然曰：“白雪纷纷何所似？”兄子胡儿曰：“撒盐空中差可拟。”兄女曰：“未若柳絮因风起。”公大笑乐。即公大兄无奕女，左将军王凝之妻也。','六年级'),
('jie-zi','诫子书','诸葛亮','三国','夫君子之行，静以修身，俭以养德。非淡泊无以明志，非宁静无以致远。夫学须静也，才须学也，非学无以广才，非志无以成学。淫慢则不能励精，险躁则不能治性。年与时驰，意与日去，遂成枯落，多不接世，悲守穷庐，将复何及！','七年级'),
('sun-quan','孙权劝学','《资治通鉴》','北宋','初，权谓吕蒙曰：“卿今当涂掌事，不可不学！”蒙辞以军中多务。权曰：“孤岂欲卿治经为博士邪！但当涉猎，见往事耳。卿言多务，孰若孤？孤常读书，自以为大有所益。”蒙乃始就学。及鲁肃过寻阳，与蒙论议，大惊曰：“卿今者才略，非复吴下阿蒙！”蒙曰：“士别三日，即更刮目相待，大兄何见事之晚乎！”肃遂拜蒙母，结友而别。','七年级'),
('mai-you','卖油翁','欧阳修','北宋','陈康肃公善射，当世无双，公亦以此自矜。尝射于家圃，有卖油翁释担而立，睨之久而不去。见其发矢十中八九，但微颔之。康肃问曰：“汝亦知射乎？吾射不亦精乎？”翁曰：“无他，但手熟尔。”康肃忿然曰：“尔安敢轻吾射！”翁曰：“以我酌油知之。”乃取一葫芦置于地，以钱覆其口，徐以杓酌油沥之，自钱孔入，而钱不湿。因曰：“我亦无他，惟手熟尔。”康肃笑而遣之。','七年级'),
('san-xia','三峡','郦道元','北魏','自三峡七百里中，两岸连山，略无阙处。重岩叠嶂，隐天蔽日，自非亭午夜分，不见曦月。至于夏水襄陵，沿溯阻绝。或王命急宣，有时朝发白帝，暮到江陵，其间千二百里，虽乘奔御风，不以疾也。春冬之时，则素湍绿潭，回清倒影。绝巘多生柽柏，悬泉瀑布，飞漱其间，清荣峻茂，良多趣味。每至晴初霜旦，林寒涧肃，常有高猿长啸，属引凄异，空谷传响，哀转久绝。故渔者歌曰：“巴东三峡巫峡长，猿鸣三声泪沾裳。”','八年级'),
('cheng-tian','记承天寺夜游','苏轼','北宋','元丰六年十月十二日夜，解衣欲睡，月色入户，欣然起行。念无与为乐者，遂至承天寺寻张怀民。怀民亦未寝，相与步于中庭。庭下如积水空明，水中藻荇交横，盖竹柏影也。何夜无月？何处无竹柏？但少闲人如吾两人者耳。','八年级'),
('da-xie','答谢中书书','陶弘景','南朝梁','山川之美，古来共谈。高峰入云，清流见底。两岸石壁，五色交辉。青林翠竹，四时俱备。晓雾将歇，猿鸟乱鸣；夕日欲颓，沉鳞竞跃。实是欲界之仙都。自康乐以来，未复有能与其奇者。','八年级'),
('zhu-yuan','与朱元思书','吴均','南朝梁','风烟俱净，天山共色。从流飘荡，任意东西。自富阳至桐庐一百许里，奇山异水，天下独绝。水皆缥碧，千丈见底。游鱼细石，直视无碍。急湍甚箭，猛浪若奔。夹岸高山，皆生寒树，负势竞上，互相轩邈；争高直指，千百成峰。泉水激石，泠泠作响；好鸟相鸣，嘤嘤成韵。蝉则千转不穷，猿则百叫无绝。鸢飞戾天者，望峰息心；经纶世务者，窥谷忘反。横柯上蔽，在昼犹昏；疏条交映，有时见日。','八年级'),
('hu-xin','湖心亭看雪','张岱','明末清初','崇祯五年十二月，余住西湖。大雪三日，湖中人鸟声俱绝。是日更定矣，余拏一小舟，拥毳衣炉火，独往湖心亭看雪。雾凇沆砀，天与云与山与水，上下一白。湖上影子，惟长堤一痕、湖心亭一点、与余舟一芥、舟中人两三粒而已。到亭上，有两人铺毡对坐，一童子烧酒炉正沸。见余，大喜曰：“湖中焉得更有此人！”拉余同饮。余强饮三大白而别。问其姓氏，是金陵人，客此。及下船，舟子喃喃曰：“莫说相公痴，更有痴似相公者！”','九年级')]
manual+=json.loads((ROOT/'data/additional-texts.json').read_text())
for wid,title,author,era,text,scope in manual:add(wid,title,author,era,text,'https://zh.wikisource.org/wiki/'+cc.convert(title),scope,'古籍学习选文 / 待逐版校对')
# Read complete, explicitly delimited learning selections from the cached ancient text.
M='\n'.join(x['content'] for x in json.loads((cache/'mengzi.json').read_text()))
for wid,title,start,end,scope in [('yu-wo','鱼我所欲也','鱼，我所欲也','此之谓失其本心','九年级'),('fu-gui','富贵不能淫','景春曰','此之谓大丈夫','八年级'),('sheng-yu','生于忧患，死于安乐','舜发于畎亩之中','死于安乐也','八年级')]:
 a=M.index(start);b=M.index(end,a)+len(end);add(wid,title,'《孟子》','战国',M[a:b]+'。','https://github.com/gujilab/chinese-classical-corpus/blob/main/output/sishu/mengzi.json',scope,'孟子原文 / gujilab (CC0)')
L='\n'.join(x['content'] for x in json.loads((cache/'lunyu.json').read_text()))
anchors=['学而时习之','吾日三省吾身','吾十有五而志于学','温故而知新','学而不思则罔','贤哉，回也','知之者不如好之者','饭疏食饮水','三人行，必有我师焉','逝者如斯夫','三军可夺帅也','博学而笃志']
lines=[]
for anchor in anchors:
 found=next((line for line in L.splitlines() if anchor in line),None)
 if not found:raise ValueError('Analects source anchor missing: '+anchor)
 lines.append(found)
add('lunyu-12','论语十二章','孔子弟子及再传弟子','先秦','\n'.join(lines),'https://github.com/gujilab/chinese-classical-corpus/blob/main/output/sishu/lunyu.json','六年级','论语原文 / gujilab (CC0)')

# Replace the three initial fragments with complete reading units, retaining old IDs for existing deep links.
for w in D['works']:
 if w['id'] in ('xueyi','loushi','ailian'):reading.append(dict(work_id=w['id'],scope='六年级' if w['id']=='xueyi' else '七年级',classification='旧样例 / 待完整选文替换',source='首批样例'))
(ROOT/'data/trial.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n');(ROOT/'data/reading-plan.json').write_text(json.dumps(reading,ensure_ascii=False,indent=2)+'\n');print('Works:',len(D['works']),'sentences:',len(D['sentences']))
