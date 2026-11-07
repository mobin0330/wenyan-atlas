"""Real UI + shared SDK + isolated fake gateway; never changes production auth."""
import threading,time,json,tempfile
from pathlib import Path
import uvicorn
from playwright.sync_api import sync_playwright
import asgi_app as site
from shared_email_auth.asgi import EmailAuthMiddleware
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.impeccable/review/0.3';OUT.mkdir(parents=True,exist_ok=True)
class Gateway:
 def validate(self,binding,token):return binding=='b'*32 and token=='t'*32
with tempfile.TemporaryDirectory()as tmp:
 original=site.atlas;site.atlas=site.TrialAtlas(Path(tmp)/'test.sqlite');site.atlas.import_file(ROOT/'data/trial.json');site.atlas.import_file(ROOT/'data/contextual-gu.json')
 server=uvicorn.Server(uvicorn.Config(EmailAuthMiddleware(site.business,site.config,gateway=Gateway()),host='127.0.0.1',port=9383,log_level='warning'));t=threading.Thread(target=server.run,daemon=True);t.start()
 for _ in range(100):
  if server.started:break
  time.sleep(.05)
 checks=[];errors=[]
 try:
  with sync_playwright()as p:
   browser=p.chromium.launch(headless=True)
   for width in [1440,390]:
    c=browser.new_context(viewport={'width':width,'height':1000 if width==1440 else 844},is_mobile=width==390,has_touch=width==390)
    def proxy(route):
     from urllib.parse import urlsplit
     u=urlsplit(route.request.url);hs={**route.request.headers,'host':'wyw.ericmo.top','x-forwarded-proto':'https','origin':'https://wyw.ericmo.top','cookie':'email_binding='+'b'*32+'; email_session='+'t'*32}
     response=route.fetch(url='http://127.0.0.1:9383'+u.path+('?' + u.query if u.query else ''),headers=hs);route.fulfill(response=response)
    c.route('https://wyw.ericmo.top/**',proxy);page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('https://wyw.ericmo.top/');page.get_by_role('heading',name='今天从哪篇课文开始？').wait_for();checks.append(f'{width}: task-first start')
    page.get_by_role('button',name='查看已比对的七上目录',exact=True).click();page.get_by_role('heading',name='当前已比对的课文 · 7 篇').wait_for();assert page.locator('.work-row').count()==7;assert '司马光'not in page.locator('.collection').inner_text();checks.append(f'{width}: no unverified text promoted to textbook')
    page.get_by_role('heading',name='陈太丘与友期行',exact=True).click();page.locator('.original').first.wait_for();assert '七年级' in page.locator('main').inner_text();assert 'p35' in page.locator('main').inner_text();checks.append(f'{width}: exact textbook trail')
    page.goto('https://wyw.ericmo.top/#map/word-39038');page.get_by_role('heading',name='一个字，不止一种理解').wait_for();page.get_by_role('button',name='文字视图',exact=True).click();page.locator('.text-map').wait_for();assert '教材注释比对' in page.locator('main').inner_text();checks.append(f'{width}: textbook gloss in word card')
    page.goto('https://wyw.ericmo.top/#words');page.get_by_role('heading',name='字词与用法',exact=True).wait_for();page.locator('#word-class').select_option(label='实词候选');page.locator('.work-row').first.wait_for();checks.append(f'{width}: word-class browsing')
    page.goto('https://wyw.ericmo.top/#read/jie-zi');page.get_by_role('link',name='练背诵',exact=True).click();page.get_by_role('heading',name='练背诵 · 诫子书').wait_for();page.locator('[data-recite-sentence]').first.uncheck();page.locator('[data-recite-sentence]').nth(3).check();expected_ids=page.locator('[data-recite-sentence]:checked').evaluate_all('(es)=>es.map(e=>e.dataset.reciteSentence)');page.get_by_role('button',name='关键词提示',exact=True).click();page.get_by_role('button',name='遮住原文回忆',exact=True).click();assert page.locator('#self-rating option[value=self_independent]').is_disabled();checks.append(f'{width}: keyword help persists into hidden mode');page.locator('[data-reveal]').first.wait_for();assert '非淡泊无以明志'not in page.locator('.recitation-sheet').inner_text();page.locator('[data-reveal]').first.click();page.locator('#self-rating').select_option('with_help');page.get_by_role('button',name='保存本次自主练习',exact=True).click();page.get_by_role('button',name='已保存自主练习',exact=True).wait_for();assert '借助提示完成' in page.locator('.practice-history').inner_text();checks.append(f'{width}: recitation selection/mask/reveal/save');page.reload();page.get_by_role('heading',name='练背诵 · 诫子书').wait_for();page.locator('.practice-history a').first.click();page.get_by_text('已恢复保存的句段范围，开始新一轮练习；历史结果保留。',exact=True).wait_for();page.locator('[data-recite-sentence]').first.wait_for();actual_ids=page.locator('[data-recite-sentence]:checked').evaluate_all('(es)=>es.map(e=>e.dataset.reciteSentence)');assert actual_ids==expected_ids;checks.append(f'{width}: exact saved selection restores after reload')
    page.locator('#toast.visible').wait_for(state='hidden');page.screenshot(path=str(OUT/f'recitation-{width}.png'),full_page=True)
    page.goto('https://wyw.ericmo.top/#progress');page.get_by_role('heading',name='我的积累',exact=True).wait_for();assert '自主背诵' in page.locator('main').inner_text();checks.append(f'{width}: separate persisted practice history')
    page.goto('https://wyw.ericmo.top/#guide');page.get_by_role('heading',name='从学校课文开始学',exact=True).wait_for();assert page.locator('main .source-item').count()==5;checks.append(f'{width}: five stories and downloadable manuals')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth');checks.append(f'{width}: no horizontal overflow')
    page.locator('#toast.visible').wait_for(state='hidden');page.screenshot(path=str(OUT/f'guide-{width}.png'),full_page=True)
    page.goto('https://wyw.ericmo.top/#library/pep54-7a-observed');page.locator('.work-row').first.wait_for();page.locator('#toast.visible').wait_for(state='hidden');page.screenshot(path=str(OUT/f'library-{width}.png'),full_page=True)
    c.close()
   assert not errors;browser.close()
 finally:server.should_exit=True;t.join(5);site.atlas=original
report={'passed':len(checks),'checks':checks,'errors':errors};(ROOT/'docs/browser-0.3.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(report)
