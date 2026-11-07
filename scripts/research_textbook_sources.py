"""Gather publicly readable source metadata for local curriculum research.
Cached third-party text is never served by the application or declared publisher-approved.
"""
import hashlib,html,json,re,time,urllib.request
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.local/textbook-research/mirrors';OUT.mkdir(parents=True,exist_ok=True)
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.a=None;self.text=[];self.title=[];self.in_title=False;self.capture=False;self.depth=0
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if t=='title':self.in_title=True
  if t=='a':self.a=[d.get('href',''),'']
  if t=='section'and 'document-text' in d.get('class',''):self.capture=True;self.depth=1
  elif self.capture and t=='section':self.depth+=1
  if self.capture and t in ['br','p','div','section']:self.text.append('\n')
 def handle_data(self,d):
  if self.a:self.a[1]+=d
  if self.capture:self.text.append(d)
  if self.in_title:self.title.append(d)
 def handle_endtag(self,t):
  if t=='a'and self.a:self.links.append(self.a);self.a=None
  if t=='title':self.in_title=False
  if self.capture and t=='section':
   self.depth-=1
   if self.depth==0:self.capture=False
  if self.capture and t in ['p','div']:self.text.append('\n')
def fetch(url):
 r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25);return r.read().decode('utf-8')
def relevant(title):return '语文'in title and '五四'in title and ('电子课本'in title or '初中课本'in title)
if __name__=='__main__':
 queue=['https://www.yeyulingfeng.com/wendang/91248584.html','https://www.yeyulingfeng.com/wendang/91242993.html'];seen=set();results=[]
 while queue and len(seen)<30:
  u=queue.pop(0)
  if u in seen:continue
  seen.add(u);key=u.split('/')[-1].split('.')[0];path=OUT/(key+'.html')
  try:
   if not path.exists():path.write_text(fetch(u));time.sleep(.2)
   raw=path.read_text();p=Extract();p.feed(raw);text=''.join(p.text).strip();(OUT/(key+'.txt')).write_text(text)
   result={'url':u,'title':''.join(p.title),'sha256':hashlib.sha256(raw.encode()).hexdigest(),'text_chars':len(text),'retrieved_at':'2026-11-05','source_kind':'third_party_public_text','authorized_for_redistribution':False}
   results.append(result);print(key,result['title'].split('_')[0],len(text),flush=True)
   for link,title in p.links:
    if relevant(title)and re.fullmatch(r'/wendang/\d+\.html',link):
     nxt='https://www.yeyulingfeng.com'+link
     if nxt not in seen and nxt not in queue:queue.append(nxt)
  except Exception as e:results.append({'url':u,'error':str(e)});print('error',u,str(e),flush=True)
 (OUT/'manifest.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
