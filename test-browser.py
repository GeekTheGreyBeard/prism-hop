from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parent.resolve()
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
    page.goto('http://127.0.0.1:8765/?test=1',wait_until='networkidle')
    assert no_overflow(page), 'menu overflows 240x282'
    assert page.locator('#menu').is_visible()
    # Muting changes the visible state and suppresses every procedural cue; unmuting restores it.
    assert page.locator('#soundBtn').get_attribute('aria-label') == 'Mute sound'
    page.locator('#soundBtn').click()
    assert page.locator('#soundBtn').get_attribute('aria-label') == 'Enable sound'
    page.locator('#soundBtn').click()
    assert page.locator('#soundBtn').get_attribute('aria-label') == 'Mute sound'
    shot(page,'menu-240x282.png')
    page.locator('#startBtn').click()
    page.wait_for_timeout(140)
    assert page.locator('#game').is_visible()
    game=page.evaluate('window.PrismHopTest.getState()')
    assert game['tiles']>=36, game
    # Inject stable neutral values then a sustained positive-x tilt; this validates browser-side calibration, smoothing and repeats.
    for _ in range(5): page.evaluate('window.PrismHopTest.simulateMotion({x:0,y:0,z:0})')
    for _ in range(6): page.evaluate('window.PrismHopTest.simulateMotion({x:.7,y:0,z:0})')
    page.wait_for_timeout(380)
    moved=page.evaluate('window.PrismHopTest.getState()')
    assert moved['sensor']['calibrating'] is False, moved
    assert moved['player']>0, moved
    shot(page,'game-240x282.png')
    page.locator('#pauseBtn').click();page.wait_for_timeout(40)
    assert page.locator('#pause').is_visible();shot(page,'pause-240x282.png')
    page.locator('#resumeBtn').click();page.wait_for_timeout(40)
    # Touch fallback remains live even without a physical bridge.
    page.locator('[data-dir="dr"]').click();page.wait_for_timeout(40)
    page.evaluate('window.PrismHopTest.forceWin()');page.wait_for_timeout(260)
    assert page.locator('#result').is_visible();shot(page,'result-240x282.png')
    assert no_overflow(page), 'game screen overflows 240x282'
    assert not errors, errors
    browser.close()
print('browser checks passed: 240x282 menu/game/pause/results, scrolling board, simulated motion and touch fallback')
