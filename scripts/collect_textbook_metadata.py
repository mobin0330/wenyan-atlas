"""Cache selected, publicly available official cover/catalog pages for local checking.
Usage: python scripts/collect_textbook_metadata.py --book-id ID --pages 1 3 4 5 6 7
The publisher catalog snapshot must already come from its normal browser UI.
Stops on unavailable/challenge responses; does not solve challenges or decrypt files.
"""
import argparse,hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'.local/textbook-research';CATALOG=ROOT/'.local/source-cache/pep-official-catalog.json'
def get_image(url,referer):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':referer}),timeout=30)as response:data=response.read()
 if not data.startswith(b'\xff\xd8'):raise ValueError('教材页不可用或出现站点验证；已停止，不将 HTML 当作教材图像。')
 return data
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--book-id',required=True);p.add_argument('--pages',type=int,nargs='+',required=True);args=p.parse_args()
 if any(n<1 or n>10 for n in args.pages):p.error('本脚本只处理封面/目录前10个阅读器页，不下载全书。')
 books=json.loads(CATALOG.read_text());book=next(b for b in books if b['id']==args.book_id and b['xk']=='语文'and b.get('xdtype')=='义务教育（五四学制）');target=CACHE/book['id'];target.mkdir(parents=True,exist_ok=True);pages=[]
 for n in sorted(set(args.pages)):
  url=book['pdfurl']+f'files/mobile/{n}.jpg';path=target/f'{n:03}.jpg'
  if not path.exists():path.write_bytes(get_image(url,book['pdfurl']+'mobile/index.html'))
  data=path.read_bytes()
  if not data.startswith(b'\xff\xd8'):raise ValueError('本地缓存不是有效的教材 JPEG，需检查来源。')
  pages.append({'reader_page':n,'url':url,'sha256':hashlib.sha256(data).hexdigest()})
 (target/'selected-pages.json').write_text(json.dumps({'book':book,'pages':pages,'usage':'只作本地核对，不公开教材扫描件'},ensure_ascii=False,indent=2));print('已核验缓存图像',len(pages))
