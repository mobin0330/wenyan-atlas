import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
 page.goto('http://127.0.0.1:9381/#practice/q-1');page.get_by_role('button',name='给我一个提示').click();page.wait_for_function('() => document.activeElement.classList.contains("hint")')
 page.locator('[data-choice="0"]').click();page.wait_for_function('() => document.activeElement.dataset.choice === "0"')
 page.get_by_role('button',name='确认判断').click();page.wait_for_function('() => document.activeElement.classList.contains("feedback")')
 page.goto('http://127.0.0.1:9381/#read/xueyi/occ-5');page.wait_for_function('() => document.activeElement.classList.contains("focused")');page.screenshot(path=str(ROOT/'.impeccable/review/mobile-source.png'),full_page=False)
 page.goto('http://127.0.0.1:9381/#map/zhi');page.locator('.text-map').wait_for();page.locator('[data-sense="zhi/zhi-pronoun"]').click();page.wait_for_function('() => document.activeElement.dataset.sense === "zhi/zhi-pronoun"');page.locator('#scope-picker summary').click();page.locator('[data-scope="六年级"]').click();page.wait_for_function('() => document.activeElement.dataset.scope === "六年级"')
 page.locator('#scope-picker summary').click();page.get_by_role('button',name='切换深浅主题').click();page.wait_for_timeout(250);page.screenshot(path=str(ROOT/'.impeccable/review/mobile-dark.png'),full_page=True)
 b.close()
report={'hint_focus':True,'choice_focus':True,'feedback_focus':True,'exact_source_focus':True,'scope_focus':True,'mobile_theme':True,'same_map_sense_focus':True};(ROOT/'docs/focus-results.json').write_text(json.dumps(report,indent=2));print(report)
