"""Semantic reading of tasks in the named observed copies; no teacher approval implied."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FULL=set('司马光|守株待兔|精卫填海|王戎不取道旁李|囊萤夜读|古人谈读书|自相矛盾|杨氏之子|两小儿辩日|论语十二章|诫子书|陋室铭|爱莲说|三峡|答谢中书书|记承天寺夜游|与朱元思书|得道多助，失道寡助|生于忧患，死于安乐|桃花源记|小石潭记|北冥有鱼|虽有嘉肴|大道之行也|马说|岳阳楼记|醉翁亭记|鱼我所欲也|曹刿论战|出师表'.split('|'))
def main():
 items=json.loads((ROOT/'data/textbook-content-inventory.json').read_text())['items'];requirements=[]
 for p in items:
  title=p['title'];tasks=[];status='awaiting_exact_requirement_check';notes='未确认该篇是否必背/必默；自主练习不能替代教材任务依据。'
  if title in FULL:tasks.append({'type':'recite','range':'全文','object':title});status='explicit_in_observed_copy';notes='所见版本课后任务明确涉及本篇；学校当前版与教师安排仍待核对。'
  if title in ['陋室铭','爱莲说']:tasks.append({'type':'dictation','range':'全文','object':title})
  if title=='富贵不能淫':tasks=[{'type':'recite','range':'指定片段','start_anchor':'居天下之广居','end_anchor':'此之谓大丈夫','object':title}];status='explicit_in_observed_copy';notes='所见版本要求指定片段，不能改为全文必背。'
  if title=='送东阳马生序':tasks=[{'type':'recite','range':'前两段','object':title}];status='explicit_in_observed_copy';notes='段落划分以该版课文为准，不能用数据库句段序号代替。'
  if title in ['铁杵成针','曹冲称象']:tasks=[{'type':'read','range':'本篇','object':title}];status='group_instruction_disambiguated';notes='合篇中的背诵指令指向另一子篇，不能继承为本篇必背。'
  if title in ['学弈','关尹子教射']:tasks=[{'type':'read_fluently','range':'本篇','object':title}];status='observed_reading_instruction';notes='所见修订本强调熟读、理解与讨论，未据此设置全文必背。'
  requirements.append({'inventory_id':p['id'],'title':title,'grade':p['grade'],'semester':p['semester'],'source_url':p['source_url'],'source_sha256':p['source_sha256'],'location':'所见教材本课课后任务（精确图像页码待交叉核对）','status':status,'tasks':tasks,'school_current_edition_confirmed':False,'teacher_reviewed':False,'notes':notes})
 (ROOT/'data/textbook-learning-requirements.json').write_text(json.dumps({'checked_at':'2026-11-05','notice':'所见版本学习要求的语义整理，不是学校当前版或教学大纲最终审核结果。不自动同步学习记录。','items':requirements},ensure_ascii=False,indent=2));print('requirements',len(requirements))
if __name__=='__main__':main()
