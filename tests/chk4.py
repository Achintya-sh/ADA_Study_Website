# Browser functional test for the v4 additions (needs playwright + chromium).
import os, asyncio, json
from playwright.async_api import async_playwright
PAGE = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dist', 'index.html'))
OUT = os.environ.get('SHOTS', '/tmp/shots'); os.makedirs(OUT, exist_ok=True)
async def main():
    fails = []
    def check(cond, msg):
        print(('ok   ' if cond else 'FAIL ') + msg)
        if not cond: fails.append(msg)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1300, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
        pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' and 'ERR_NAME' not in m.text else None)
        await pg.add_init_script("localStorage.clear()")
        await pg.goto(PAGE); await pg.wait_for_timeout(1500)
        await pg.add_style_tag(content='html{scroll-behavior:auto!important}')
        # --- sidebar numbering and progress
        nums = await pg.evaluate("[...document.querySelectorAll('#navLines .num')].map(e=>e.textContent)")
        check(len(nums) == len(set(nums)), 'sidebar numbers are unique (%d entries)' % len(nums))
        check(all(('X%d' % i) in nums for i in range(1, 9)), 'exam-prep stops are labelled X1..X8')
        check(await pg.evaluate("document.getElementById('progTxt').textContent") == '0 of 29 stops understood', 'progress counts 29 stops')
        # --- hero map
        ids = await pg.evaluate("[...document.querySelectorAll('#mapDots circle')].map(c=>c.dataset.id)")
        check(all(('ch%d' % i) in ids for i in range(11, 18)), 'hero map has dots for stops 11-17')
        inside = await pg.evaluate("[...document.querySelectorAll('#mapDots circle')].every(c=>+c.getAttribute('cx')<=940 && +c.getAttribute('cy')<=200)")
        check(inside, 'all hero dots lie inside the map')
        # --- new stops and quizzes
        for sid, n in (('ch12', 19), ('ch11', 10), ('ch15', 6), ('ch16', 8), ('ch17', 5)):
            c = await pg.evaluate("document.querySelectorAll('#%s .quiz .q').length" % sid)
            check(c == n, 'quiz questions mounted in %s: %d (expected %d)' % (sid, c, n))
        for sid in ('ch12', 'ch15', 'ch16', 'ch17', 'ch10', 'ch11'):
            blocks = await pg.evaluate("document.querySelectorAll('#%s pre.code').length" % sid)
            check(blocks > 0, '%s shows code blocks (%d)' % (sid, blocks))
        # --- bug hunts (new items start at index 13)
        nb = await pg.evaluate('BUGS.length')
        check(nb == 18 + 8, 'bug hunts: %d items (18 old + 8 new)' % nb)
        for i in range(18, nb):
            a0 = await pg.evaluate('BUGS[%d].a[0]' % i)
            card = pg.locator('#bugList .drill').nth(i)
            await card.locator('.bugline[data-k="%d"]' % a0).click()
            fb = await card.locator('.dfb').inner_text()
            check('Found it' in fb and 'undefined' not in fb, 'bug %d accepts its flagged line and shows a fix' % (i + 1))
            wrong = await pg.evaluate('[...Array(BUGS[%d].c.length).keys()].find(k => !BUGS[%d].a.includes(k))' % (i, i))
        # a clean wrong click on a fresh card
        await pg.click('#bugReset')
        card = pg.locator('#bugList .drill').nth(18)
        wk = await pg.evaluate('[...Array(BUGS[18].c.length).keys()].find(k => !BUGS[18].a.includes(k))')
        await card.locator('.bugline[data-k="%d"]' % wk).click()
        check('is fine' in await card.locator('.dfb').inner_text(), 'bug hunt rejects a correct line')
        # --- blanks (new items start at index 18)
        nbl = await pg.evaluate('BLANKS.length')
        check(nbl == 28 + 7, 'fill-in drills: %d items (28 old + 7 new)' % nbl)
        for i in range(28, nbl):
            ans = await pg.evaluate("(BLANKS[%d].c.match(/\\{\\{(.*?)\\}\\}/g) || []).map(s => s.slice(2, -2).split('|')[0])" % i)
            card = pg.locator('#blankList .drill').nth(i)
            inputs = card.locator('input.blank')
            check(await inputs.count() == len(ans), 'blank drill %d has %d inputs' % (i + 1, len(ans)))
            for k, a in enumerate(ans):
                await inputs.nth(k).fill(a)
            await card.locator('[data-a="check"]').click()
            check('All correct' in await card.locator('.dfb').inner_text(), 'blank drill %d accepts the right answers' % (i + 1))
        # --- ordering puzzles (new items start at index 8)
        npz = await pg.evaluate('PARSONS.length')
        check(npz == 9 + 4, 'ordering puzzles: %d items (9 old + 4 new)' % npz)
        for i in range(9, npz):
            n = await pg.evaluate('PARSONS[%d].c.length' % i)
            alts = await pg.evaluate('[Array.from({length: PARSONS[%d].c.length}, (_, k) => k), ...(PARSONS[%d].ok || [])]' % (i, i))
            for oi, order in enumerate(alts):
                card = pg.locator('#parList .drill').nth(i)
                await card.locator('[data-a="reset"]').click()
                for k in order:
                    await card.locator('[data-r="pool"] .bugline[data-k="%d"]' % k).click()
                await card.locator('[data-a="check"]').click()
                good = 'Correct order' in await card.locator('.dfb').inner_text()
                check(good, 'puzzle %d accepts %s order' % (i + 1, 'the listed' if oi == 0 else 'alternative %d' % oi))
        # --- mock exam
        await pg.click('#mockStart'); await pg.wait_for_timeout(300)
        qs = pg.locator('#mockBox .q'); nq = await qs.count()
        check(nq == 20, 'mock exam draws 20 questions')
        for i in range(nq):
            await qs.nth(i).locator('.opt').first.click()
        await pg.wait_for_timeout(300)
        res = await pg.inner_text('#mockResult')
        check(len(res) > 20, 'mock exam shows a result')
        deck = await pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('ada-deck') || '{}')).length")
        check(deck > 0, 'wrong mock answers reach My mistakes (%d)' % deck)
        # --- LeetCode mock widget
        lab = pg.locator('.lab[data-w="mocklc"]'); await lab.scroll_into_view_if_needed()
        check(await lab.locator('table tr').count() == 4, 'LC mock shows header + 3 problems')
        links = await lab.locator('a').evaluate_all('els => els.map(e => e.href)')
        check(all(l.startswith('https://leetcode.com/problems/') for l in links) and len(links) == 3, 'LC mock links: %s' % links[:1])
        await lab.locator('button', has_text='Start').click(); await pg.wait_for_timeout(700)
        for s in await lab.locator('table select').all(): await s.select_option('2')
        cap = await lab.locator('.cap').inner_text()
        check('240 of 240' in cap, 'LC mock scores full marks: ' + cap[:40])
        await pg.screenshot(path=OUT + '/lc_mock.png', clip=await lab.bounding_box())
        # --- quick review mode
        await pg.click('#quickBtn'); await pg.wait_for_timeout(300)
        for sid in ('ch11', 'ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17'):
            vis = await pg.evaluate("[...document.querySelectorAll('#%s > *')].filter(e => getComputedStyle(e).display !== 'none').map(e => e.className || e.tagName)" % sid)
            check(any('idea' in v for v in vis) and not any('code' in v or 'tbl-wrap' in v or 'lab' in v for v in vis) and len(vis) <= 8, 'quick review %s keeps idea/traps only: %s' % (sid, vis))
        await pg.click('#quickBtn')
        # --- screenshots for a visual check
        await pg.evaluate("window.scrollTo(0,0)"); await pg.screenshot(path=OUT + '/hero.png', clip={'x': 0, 'y': 0, 'width': 1300, 'height': 520})
        for sid in ('ch12', 'ch16', 'ch15', 'ch17'):
            el = pg.locator('#' + sid); await el.scroll_into_view_if_needed()
            await pg.screenshot(path=OUT + '/%s.png' % sid, clip={'x': 0, 'y': 0, 'width': 1300, 'height': 900})
        mob = await b.new_page(viewport={'width': 390, 'height': 800})
        await mob.goto(PAGE + '#ch12'); await mob.wait_for_timeout(800)
        await mob.screenshot(path=OUT + '/mobile_ch12.png')
        overflow = await mob.evaluate("document.documentElement.scrollWidth > innerWidth + 2")
        check(not overflow, 'no sideways scroll on a 390px phone')
        check(not errs, 'no page errors %s' % errs[:3])
        await b.close()
    print('\nFAILED:' if fails else '\nALL BROWSER CHECKS PASSED', fails or '')
asyncio.run(main())
