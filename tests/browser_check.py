"""Run with an existing Python environment containing Playwright; no app dependencies."""
import json,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.impeccable/review';OUT.mkdir(parents=True,exist_ok=True)
results=[]
def check(name,condition):
 if not condition:raise AssertionError(name)
 results.append({'check':name,'passed':True})
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 start=time.monotonic();page.goto('http://127.0.0.1:9381');page.get_by_role('heading',name='一个字，不止一种理解').wait_for();load_ms=(time.monotonic()-start)*1000
 check('desktop renders actual graph',page.locator('#graph-svg .node').count()>5)
 check('default scope primary only',page.locator('[data-scope][aria-pressed=true]').count()==1)
 page.locator('[data-scope="小学"]').click();check('at least one scope retained',page.locator('[data-scope][aria-pressed=true]').count()==1)
 page.locator('[data-scope="六年级"]').click();page.reload();page.get_by_role('heading',name='一个字，不止一种理解').wait_for();check('scope survives reload',page.locator('[data-scope][aria-pressed=true]').count()==2)
 page.screenshot(path=str(OUT/'desktop.png'),full_page=True)
 before=page.locator('#graph-svg').get_attribute('viewBox');page.get_by_role('button',name='放大地图').click();check('zoom changes viewbox',page.locator('#graph-svg').get_attribute('viewBox')!=before);page.get_by_role('button',name='复位',exact=True).click()
 page.locator('[data-node-sense="zhi-of"]').click();page.get_by_role('heading',name='连接修饰关系',exact=True).wait_for();check('sense changes evidence',page.locator('.evidence .citation').count()==2)
 page.get_by_role('link',name='回到原文',exact=True).first.click();page.locator('.original').first.wait_for();check('return to exact original',page.locator('.sentence.focused').count()==1)
 page.locator('.word-link').first.click();page.get_by_role('heading',name='一个字，不止一种理解').wait_for();check('original to knowledge map',True)
 page.get_by_role('button',name='文字视图',exact=True).click();page.locator('.text-map').wait_for();check('in-place view toggle retains focus',page.evaluate('document.activeElement.dataset.view')=='text');check('accessible text alternative',page.locator('.text-map').count()==1)
 page.locator('#query').fill('学弈');page.get_by_role('button',name='搜索',exact=True).click();page.get_by_role('heading',name='搜索结果').wait_for();check('search finds work',page.locator('.search-result').count()==1)
 page.locator('#query').fill('无此内容zz');page.get_by_role('button',name='搜索',exact=True).click();page.get_by_role('heading',name='暂时没找到').wait_for();check('search empty state',True)
 page.goto('http://127.0.0.1:9381/#practice/q-1');page.get_by_role('button',name='确认判断').wait_for();check('answer hidden until submission',page.locator('.feedback').count()==0)
 page.get_by_role('button',name='给我一个提示',exact=True).click();page.locator('.hint').wait_for();page.locator('[data-choice="0"]').click();page.get_by_role('button',name='确认判断',exact=True).click();page.locator('.feedback').wait_for();check('hinted answer feedback', '这一次判断正确' in page.locator('.feedback').inner_text());
 page.goto('http://127.0.0.1:9381/#progress');page.get_by_role('heading',name='我的积累',exact=True).wait_for();check('hint is not independent mastery','借助提示完成' in page.locator('main').inner_text());page.screenshot(path=str(OUT/'progress.png'),full_page=True)
 page.goto('http://127.0.0.1:9381/#library');page.get_by_role('button',name='查看教材目录状态').click();page.get_by_role('heading',name='这个范围还没有已核验篇目').wait_for();check('published catalog does not fake coverage',True);page.get_by_role('button',name='浏览独立原典样例').click();page.locator('.work-row').first.wait_for()
 page.goto('http://127.0.0.1:9381/#sources');page.get_by_role('heading',name='每一条关系，都应有来处').wait_for();check('coverage explicit 18 pending slots',page.locator('.coverage-cell').count()==18)
 page.goto('http://127.0.0.1:9381/#map/zhi');page.get_by_role('heading',name='一个字，不止一种理解').wait_for();page.locator('#theme').click();page.wait_for_timeout(250);page.screenshot(path=str(OUT/'dark.png'),full_page=True);check('dark theme selectable',page.locator('html').get_attribute('data-theme')=='dark');page.locator('#theme').click()
 for width in (390,768):
  context=browser.new_context(viewport={'width':width,'height':844 if width==390 else 1024},device_scale_factor=1,is_mobile=width==390,has_touch=width==390)
  mobile=context.new_page();mobile.goto('http://127.0.0.1:9381');mobile.get_by_role('heading',name='一个字，不止一种理解').wait_for()
  check(str(width)+'px no horizontal overflow',mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'))
  if width==390:check('mobile starts with text-first map',mobile.locator('.text-map').count()==1)
  if width==768:check('tablet text-first, graph opt-in',mobile.locator('.text-map').count()==1)
  if width==390:
   check('mobile scope disclosure starts collapsed',not mobile.locator('#scope-picker').evaluate('(e)=>e.open'))
   mobile.get_by_role('button',name='切换深浅主题').click();check('mobile theme remains available',mobile.locator('html').get_attribute('data-theme')=='dark');mobile.get_by_role('button',name='切换深浅主题').click();mobile.wait_for_timeout(250)
  mobile.screenshot(path=str(OUT/('mobile.png' if width==390 else 'tablet.png')),full_page=True)
  mobile.get_by_role('link',name='辨析练习',exact=True).click();mobile.get_by_role('button',name='确认判断').wait_for();mobile.locator('[data-choice="2"]').click();mobile.get_by_role('button',name='确认判断').click();mobile.locator('.feedback').wait_for();check(str(width)+'px wrong answer gives hypothesis', '可能' in mobile.locator('.feedback').inner_text());check(str(width)+'px practice no overflow',mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'))
  mobile.goto('http://127.0.0.1:9381/#read/xueyi/occ-5');mobile.locator('.sentence.focused').wait_for();mobile.wait_for_timeout(100);check(str(width)+'px exact later source is visible',mobile.locator('.sentence.focused').evaluate('(e)=>{const r=e.getBoundingClientRect();return r.top>=0&&r.top<innerHeight}'));check(str(width)+'px exact source has focus',mobile.evaluate('document.activeElement.classList.contains("focused")'))
  mobile.get_by_role('link',name='按课本学',exact=True).click();mobile.locator('.work-row').first.click();mobile.locator('.original').first.wait_for();check(str(width)+'px reader no overflow',mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'))
  context.close()
 check('no JavaScript or CSP errors',not errors)
 browser.close()
report={'passed':len(results),'load_ms':round(load_ms,1),'checks':results,'browser_errors':errors};(ROOT/'docs/browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
