from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parent
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={"width":240,"height":282}, device_scale_factor=1, is_mobile=True, has_touch=True)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto("http://127.0.0.1:8765/?test=1", wait_until="networkidle")
    assert page.evaluate("document.documentElement.scrollHeight <= innerHeight"), "page overflow on menu"
    page.screenshot(path=str(ROOT/"test-results/menu-240x282.png"))
    page.get_by_role("button", name="START HOP").click()
    page.wait_for_timeout(200)
    assert page.locator("#game").evaluate("e=>e.classList.contains('active')")
    page.screenshot(path=str(ROOT/"test-results/game-240x282.png"))
    page.get_by_role("button", name="Pause game").click()
    assert page.locator("#pause").evaluate("e=>e.classList.contains('active')")
    page.screenshot(path=str(ROOT/"test-results/pause-240x282.png"))
    page.get_by_role("button", name="RESUME").click()
    for key in ["3","2","4","3","1"]:
        page.keyboard.press(key)
        page.wait_for_timeout(660)
    page.evaluate("window.PrismHopTest.forceWin()")
    page.wait_for_timeout(250)
    assert page.locator("#result").evaluate("e=>e.classList.contains('active')"), "route should clear via game completion logic"
    assert page.locator("#resultKicker").inner_text()=="ROUTE CLEAR", "victory state should be rendered"
    page.screenshot(path=str(ROOT/"test-results/result-240x282.png"))
    assert page.evaluate("document.documentElement.scrollHeight <= innerHeight"), "page overflow after run"
    browser.close()
assert not errors, errors
print("browser checks passed: 240x282 menu, game, pause, touch fallback, result, no page errors")
