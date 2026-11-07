"""Isolated authenticated UI test. The fake gateway exists only on loopback:9383."""
import threading,time,json,tempfile,sys
from pathlib import Path
import uvicorn
from playwright.sync_api import sync_playwright
import asgi_app as site
from shared_email_auth.asgi import EmailAuthMiddleware
ROOT=Path(__file__).resolve().parents[1]
class Gateway:
 def validate(self,binding,token):return binding=='b'*32 and token=='t'*32
with tempfile.TemporaryDirectory() as tmp:
 original=site.atlas;site.atlas=site.TrialAtlas(Path(tmp)/'test.sqlite');site.atlas.import_file(ROOT/'data/trial.json')
 app=EmailAuthMiddleware(site.business,site.config,gateway=Gateway());server=uvicorn.Server(uvicorn.Config(app,host='127.0.0.1',port=9383,log_level='warning'));thread=threading.Thread(target=server.run,daemon=True);thread.start()
 for _ in range(100):
  if server.started:break
  time.sleep(.05)
 results={}
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(headless=True);context=browser.new_context(viewport={'width':1440,'height':1000})
   def proxy(route):
    from urllib.parse import urlsplit
    u=urlsplit(route.request.url);headers={**route.request.headers,'host':'wyw.ericmo.top','x-forwarded-proto':'https','origin':'https://wyw.ericmo.top','cookie':'email_binding='+'b'*32+'; email_session='+'t'*32}
    response=route.fetch(url='http://127.0.0.1:9383'+u.path+('?' + u.query if u.query else ''),headers=headers);route.fulfill(response=response)
   context.route('https://wyw.ericmo.top/**',proxy);page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto('https://wyw.ericmo.top/');page.get_by_role('heading',name='一个字，不止一种理解').wait_for();results['authenticated_boot_with_shared_client']=True
   page.get_by_role('link',name='按课本学',exact=True).click();page.locator('.work-row').first.wait_for();results['primary_units']=page.locator('.work-row').count();assert results['primary_units']>=8
   for scope in ['六年级','七年级','八年级','九年级']:
    page.locator('[data-scope="'+scope+'"]').click();page.wait_for_timeout(100)
   page.locator('.work-row').last.wait_for();results['all_scopes_units']=page.locator('.work-row').count();assert results['all_scopes_units']>=44
   page.screenshot(path=str(ROOT/'.impeccable/review/expanded-library.png'),full_page=True)
   page.goto('https://wyw.ericmo.top/#read/yue-yang');page.locator('.original').first.wait_for();results['long_complete_reader']=len(page.locator('main').inner_text())>500
   page.goto('https://wyw.ericmo.top/#practice');page.get_by_role('button',name='确认判断').wait_for();page.locator('[data-choice="0"]').click();page.get_by_role('button',name='确认判断').click();page.locator('.feedback').wait_for();page.goto('https://wyw.ericmo.top/#progress');page.get_by_role('heading',name='我的积累',exact=True).wait_for();results['server_records_after_attempt']='1' in page.locator('main').inner_text();results['browser_errors']=errors;assert not errors;browser.close()
 finally:server.should_exit=True;thread.join(5);site.atlas=original
(ROOT/'docs/trial-browser-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(results)
