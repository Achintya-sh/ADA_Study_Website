import os
import asyncio, re
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1300,'height':900})
        errs=[]
        pg.on('pageerror', lambda e: errs.append('PAGEERR '+str(e)))
        pg.on('console', lambda m: errs.append('CONSOLE '+m.text) if m.type=='error' and 'ERR_NAME' not in m.text else None)
        await pg.goto('file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dist', 'index.html'))); await pg.wait_for_timeout(1500)
        print('errors:', errs or 'none')
        print('lab failures:', await pg.evaluate("[...document.querySelectorAll('.lab-b > .cap.bad')].map(e=>e.closest('.lab').dataset.w+': '+e.textContent.slice(0,60))"))
        print('groups:', await pg.evaluate("[...document.querySelectorAll('#navLines .line-group h4')].map(e=>e.textContent)"))
        print('progress:', await pg.evaluate("document.getElementById('progTxt').textContent"))
        print('ladder rows:', await pg.evaluate("document.querySelectorAll('.lab[data-w=ladder2] table tr').length-1"))
        print('stats:', await pg.evaluate("[...document.querySelectorAll('.lab[data-w=ladder2] .stat')].map(e=>e.textContent)"))
        print('tierbars:', await pg.evaluate("[...document.querySelectorAll('.tb .tbn')].map(e=>e.textContent)"))
        print('quizzes mounted:', await pg.evaluate("['ch3','ch4','ch5','ch6','ch8','ch10','ch11','ch12','ch13','ch14'].map(k=>k+':'+document.querySelectorAll('#'+k+' .quiz .q').length)"))
        print('code blocks per stop:', await pg.evaluate("['ch3','ch4','ch5','ch6','ch8','ch10','ch11','ch12','ch13','ch14','ladder'].map(k=>k+':'+document.querySelectorAll('#'+k+' pre.code').length)"))
        print('unfilled placeholders:', await pg.evaluate("document.body.innerHTML.includes('{{code:')"))
        # dead internal links
        dead = await pg.evaluate("[...new Set([...document.querySelectorAll('a[href^=\"#\"]')].map(a=>a.getAttribute('href')).filter(h=>h.length>1 && !document.getElementById(h.slice(1))))]")
        print('dead links:', dead)
        txt = await pg.evaluate("document.body.innerText")
        for pat in [r'\bC[1-5]\b', r'\bE[0-4]\b', r'Contest line', r'contest line', r'Tonight and tomorrow', r'end-sem line', r'End-sem line', r'zerotrac']:
            for m in re.finditer(pat, txt):
                print('STALE', pat, '::', txt[max(0,m.start()-60):m.end()+60].replace('\n',' '))
        await b.close()
asyncio.run(main())
