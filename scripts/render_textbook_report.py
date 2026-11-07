"""Render the full-range curriculum research ledger from structured evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 registry=json.loads((ROOT/'data/textbook-register.json').read_text());items=json.loads((ROOT/'data/textbook-content-inventory.json').read_text())['items'];req={x['inventory_id']:x for x in json.loads((ROOT/'data/textbook-learning-requirements.json').read_text())['items']}
 out=['# 全学段教材来源与内容梳理','核查日期：2026-11-05。范围锁定：上海五四学制、人民教育出版社语文，一至九年级上下册，共18个册位。','## 本轮实际完成与尚未完成','已从人教社正常浏览器目录确认18册官方入口，逐册登记教材文档线索，并保存18册第三方目录候选。已从所见教材文档中登记52个文言散文篇目/子篇观察条目，定位其正文标题，整理注释词头候选和学习任务。古人谈读书暂按一课计，合篇按子篇拆分。','**52不是当前上海教材文言文总数，更不是52篇全部通过词义审核。** 所见文档包含不同修订时期，用户已确认全册采用最新正式修订版；具体新版资料同版性仍由实施方核实。18个入口齐全，与18册当前版逐页核完，是两种不同的完成状态。现有网站的教材认证状态与学习记录本轮没有被这些候选数据自动改写。','首次打开官方阅读器应从[人教社教材目录](https://jc.pep.com.cn/)选择“义务教育（五四学制）→语文→年级→在线阅读”。本轮曾正常打开阅读器，后来部分请求出现站点验证，已停止相关自动读取；没有解密、解验证码或规避验证。只有实际取得的图像才计作来源证据。','## 18册总表','“所见条目”来自下方链接的教材副本，仅对应那个副本。低年级暂未发现独立文言散文不等于没有古诗词、蒙学韵文，也不等于已核清当前版无篇目。','| 年级/册次 | 官方电子教材 | 所见教材文档 | 文言散文观察条目 | 与目标最新版同版性 |','|---|---|---|---|---|']
 for b in registry['books']:
  ws=[x for x in items if x['grade']==b['grade']and x['semester']==b['semester']];titles='、'.join(x['title']for x in ws)or'所见版本暂未发现独立文言散文；当前版待核'
  out.append(f"| {b['grade']}{b['semester']} | [官方入口]({b['official_reader_url']}) | [所见副本]({b['observed_textbook_copy']['url']}) | {titles} | 未确认 |")
 out+=['## 已发现的版次与来源冲突','已决定采用最新正式修订版；以下差异由实施方按来源解决，不再等待用户选版，也不阻塞其他已明确内容。不能把旧版课号配上新版注释。','| 篇目 | 所见旧副本位置 | 新目录候选位置 | 证据 |','|---|---|---|---|','| 精卫填海 | 四上13课，p50 | 四上12课，p50 | [2026目录候选](https://www.sohu.com/a/1084488010_120904083) |','| 王戎不取道旁李 | 四上25课，p110 | 四上23课，p102 | 同上；新目录20课标题有缺项，不补造 |','| 古人谈读书 | 五上24课，p104 | 五上23课，p102 | [2026目录候选](https://www.sohu.com/a/1084690491_120904083)，第一单元首篇有缺项 |','| 三峡 | 八上10课，p54 | 八上11课，p62 | [修订本目录候选](https://www.dzskb.com/tbb54yw8sc-2024.html) |','| 桃花源记 | 八下9课，p54 | 八下9课，p62 | [修订本目录候选](https://www.dzskb.com/tbb54yw8xc-2024.html) |','六上历史目录列《伯牙鼓琴》《书戴嵩画牛》，所见修订本为《两小儿辩日》《曹冲称象》；六下历史目录与修订本也不同。这说明教材变化不只是页码，篇目本身也有调整，不能融合成一套。七下第三方文字目录夹有重复旧课名，官方已取得目录页可作清理依据。八下第三方新目录把《式微》的篇属写成《诗经·郑风》，与应继续核验的原典篇属存在冲突，因此该网页不能整页自动批准。二上所谓新版介绍页的目录为图片，未把介绍文计作目录。','## 52个篇目与学习任务底账','每条均保留具体教材文档、年级、册、课号、目录印刷页、来源摘要和候选状态。合篇起页不能冒充子篇精确页码。下表背诵/默写任务仅对应所见副本，具体段落还需以该版原文校准；未写“必背”不代表教学大纲没有要求。','| 年级/册 | 篇目 | 所见课号 / 页码 | 已整理的学习要求 | 当前产品候选文本 |','|---|---|---|---|---|']
 for w in items:
  r=req[w['id']];tasks=[]
  for t in r['tasks']:
   label={'recite':'背诵','dictation':'默写','read':'朗读','read_fluently':'熟读'}[t['type']];tasks.append(label+'：'+t['range'])
  task='；'.join(tasks)or'具体背诵/默写要求待核'
  out.append(f"| {w['grade']}{w['semester']} | [{w['title']}]({w['source_url']}) | {w['lesson']} / p{w['printed_page']}（{w['page_scope']}） | {task} | {'已有候选，未完成教材校准'if w['existing_trial_work_id']else'尚未收录'} |")
 out+=['## 实词、虚词与其他知识如何梳理','实词、虚词是教学归类层，具体词性与本句语法功能另列；代词、副词等归类可能随教学体系而不同，必须注明本产品采用的依据，不能宣称教材对每个字都给出统一分类。通假、古今异义、词类活用属于文言现象，特殊句式属于句子层，人物、事件、文化常识分别存储。','每个正式知识实例必须形成：指定教材版本 → 年级/册/单元/课文 → 段落/原句 → 词语位置 → 本处读音与义项 → 词性/语法功能 → 教材注释位置与依据 → 审核状态。一个字的多个用法不能全部套到每一句。','当前词头提取结果属于候选：包括专名、短语、同组子篇重复项及OCR误差，不是“全部实词虚词已解释”。合篇注释还没有全部分配到子篇和本句，尚未批量导入学生知识地图。','## 背诵任务的关键辨别','六上：所见版本的背诵指令指向《两小儿辩日》，不让《曹冲称象》继承。四下：背诵指令指向《囊萤夜读》，不让《铁杵成针》继承。六下：所见修订本明确熟读《学弈》《关尹子教射》，不凭旧印象加必背。七下：《陋室铭》《爱莲说》有背诵并默写要求。八上：《富贵不能淫》在所见版本要求指定片段；九下《送东阳马生序》在所见版本要求前两段。背诵和默写记录继续独立。','## 后续内容工作顺序与验收','1. 18册逐一核实最新正式修订版的版权版次，对照官方目录解决修订差异；保留旧版记录，不互相覆盖。\n2. 确认每课的古代正文选段、字形、标点、分段，古诗词和古典白话小说另列。\n3. 按本句位置逐条整理教材注释对应的义项、读音、词性、文言现象和句式，完成跨篇同义/异义归并。\n4. 核清每一条背诵、默写任务对象、范围和出处，不能由AI猜测或按合篇自动继承。\n5. 经内容审核后分批进入学生端，并给出当前指定版的实际分母和覆盖率。','本轮没有宣布上述1–5全部完成，也没有把历史目录、第三方OCR或AI候选标成人工审定知识。','## 文件与复核方法','- `data/textbook-register.json`：18册官方入口、所见教材副本、版本风险。\n- `data/textbook-directory-observations.json`：18册1098条目录层级候选，含现代文、习作、园地等，不能当作文言文数量。\n- `data/textbook-new-directory-observations.json`：新增修订版目录线索，单独保留。\n- `data/textbook-content-inventory.json`：52个文言散文观察条目与候选注释词头。\n- `data/textbook-learning-requirements.json`：52条对应学习任务整理状态。\n- `docs/TEXTBOOK-CONTENT-INVENTORY.csv`：适合逐行检查的篇目清单。\n- `docs/TEXTBOOK-DIRECTORIES.md`：全部18册目录候选，便于阅读。','教材图像和第三方全文缓存位于项目私有 `.local/textbook-research/`，不对网站开放，不作为可自由再分发材料。公开目录或可在线阅读不能自动视为注释、译文、配图再分发授权。']
 status_file=ROOT/'docs/WORK-STATUS.md'
 if status_file.exists():out.insert(1,status_file.read_text().strip())
 (ROOT/'docs/TEXTBOOK-RESEARCH.md').write_text(''.join(('\n'if i and out[i-1].startswith('|')and line.startswith('|')else'\n\n'if i else'')+line for i,line in enumerate(out))+'\n')
 catalogs=['# 18册教材目录候选全集','核查日期：2026-11-05。以下是第三方所见目录的逐册登记，包含历史版本，**不是当前学校18册目录已逐项核准的声明**。同题名现代改写、古诗词和文言散文应另行分类。教材副本中的课号若与此处冲突，以版本对应的教材原页核对，不能直接融合。']
 for b in registry['books']:
  d=b['directory_observation'];catalogs+=[f"## {b['grade']}年级{b['semester']}册",f"[官方入口]({b['official_reader_url']}) · [本目录候选来源]({d['url']})\n\n{d['edition']}",'\n'.join('- '+x for x in d['entries'])]
  for extra in b['additional_directory_observations']:
   if extra['lines']:catalogs+=[f"### 修订目录另存\n\n[来源]({extra['url']}) · {extra['edition_claim']}\n\n注意缺项、OCR错字与篇属冲突，未自动替换上方目录。",'\n'.join('- '+x for x in extra['lines'])]
 (ROOT/'docs/TEXTBOOK-DIRECTORIES.md').write_text('\n\n'.join(catalogs)+'\n');print('reports rendered')
if __name__=='__main__':main()
