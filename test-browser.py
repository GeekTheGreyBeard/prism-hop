from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parent.resolve()
BASE_URL=os.environ.get('RBERT_BASE_URL','http://127.0.0.1:8765')
OUT=ROOT/'test-results'
OUT.mkdir(exist_ok=True)

def shot(page,name):
    page.screenshot(path=str(OUT/name),full_page=True)

def no_overflow(page):
    return page.evaluate('document.documentElement.scrollWidth<=240 && document.documentElement.scrollHeight<=282')

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':240,'height':282},has_touch=True)
    errors=[]
    page.on('pageerror',lambda err: errors.append(str(err)))
    page.goto(BASE_URL.rstrip('/')+'/?test=1',wait_until='networkidle')
    assert no_overflow(page), 'menu overflows 240x282'
    assert page.locator('#menu').is_visible()
    # Muting changes the visible state and suppresses every procedural cue; unmuting restores it.
    assert page.locator('#soundBtn').get_attribute('aria-label') == 'Mute sound'
    page.locator('#soundBtn').click()
    assert page.locator('#soundBtn').get_attribute('aria-label') == 'Enable sound'
    page.locator('#soundBtn').click()
    assert page.locator('#soundBtn').get_attribute('aria-label') == 'Mute sound'
    shot(page,'menu-240x282.png')
    page.locator('#helpBtn').click()
    assert page.locator('#help').is_visible()
    assert no_overflow(page), 'help overflows 240x282'
    page.locator('#backBtn').click()
    page.locator('#startBtn').click()
    page.wait_for_timeout(140)
    assert page.locator('#game').is_visible()
    game=page.evaluate('window.RBertTest.getState()')
    assert game['tiles']>=36, game
    # Inject stable neutral values then a sustained positive-x tilt; this validates browser-side calibration, smoothing and repeats.
    for _ in range(5): page.evaluate('window.RBertTest.simulateMotion({x:0,y:0,z:0})')
    for _ in range(6): page.evaluate('window.RBertTest.simulateMotion({x:.7,y:0,z:0})')
    page.wait_for_timeout(380)
    moved=page.evaluate('window.RBertTest.getState()')
    assert moved['sensor']['calibrating'] is False, moved
    assert moved['player']>0, moved
    shot(page,'game-240x282.png')
    page.locator('#pauseBtn').click();page.wait_for_timeout(40)
    assert page.locator('#pause').is_visible();shot(page,'pause-240x282.png')
    page.locator('#resumeBtn').click();page.wait_for_timeout(40)
    # The control plane is deliberately invisible: dragging from the hopper toward a corner hops;
    # a double tap on the same field fires Phase without a visible direction pad.
    pad=page.locator('#gesturePad')
    box=pad.bounding_box();assert box and box['width']==230 and box['height']==190, box
    assert [page.evaluate(f'window.RBertTest.gestureDirection({x},{y})') for x,y in [(1,1),(229,1),(1,189),(229,189)]] == ['ul','ur','dl','dr']
    page.mouse.move(box['x']+115,box['y']+74);page.mouse.down();page.mouse.move(box['x']+205,box['y']+132,steps=2);page.mouse.up();page.wait_for_timeout(40)
    page.mouse.dblclick(box['x']+118,box['y']+74);page.wait_for_timeout(60)
    assert page.locator('#phaseState').inner_text() == 'ACTIVE'
    page.evaluate('window.RBertTest.forceWin()');page.wait_for_timeout(260)
    assert page.locator('#result').is_visible();shot(page,'result-240x282.png')
    assert no_overflow(page), 'game screen overflows 240x282'
    # Chromium rendering budget check only; this is not a physical R1 frame-rate result.
    frames=page.evaluate('''() => new Promise(resolve => { const samples=[]; let prev=performance.now(); function tick(t){samples.push(t-prev);prev=t;if(samples.length===45)resolve(samples);else requestAnimationFrame(tick)}requestAnimationFrame(tick) })''')
    frames.sort();assert frames[int(len(frames)*.90)] < 50, frames
    assert not errors, errors
    browser.close()
print('browser checks passed: 240x282 menu/game/pause/results, scrolling board, motion, gesture fallback, and Chromium frame pacing')
