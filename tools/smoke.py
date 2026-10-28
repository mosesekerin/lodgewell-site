import asyncio, os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':400,'height':860})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath('old/index.html')); await pg.wait_for_timeout(400)
        print('all:', await pg.inner_text('#count'))
        await pg.select_option('#f-gender','male'); await pg.select_option('#f-split','2'); await pg.fill('#f-max','260k')
        for a in ['Campus Gate','Oduduwa Estate']: await pg.click(f'#f-areas label:has-text("{a}")')
        print('filtered:', await pg.inner_text('#count'))
        await pg.click('#list .card [data-act=req]'); await pg.wait_for_timeout(100)
        print((await pg.inner_text('#list .card pre'))[:160].replace('\n',' / '))
        await pg.screenshot(path='/tmp/claude-0/-home-claude/099aa447-b20f-5ba7-88af-b8d897598eea/scratchpad/site-phone.png')
        print('errors:', errs); await b.close()
asyncio.run(main())
