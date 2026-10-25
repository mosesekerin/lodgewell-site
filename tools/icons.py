import asyncio, os
from playwright.async_api import async_playwright
R=os.path.dirname(os.path.abspath(__file__)); A=os.path.join(R,'..','assets')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1200,'height':630}); await pg.goto('file://'+os.path.join(R,'og.html')); await pg.wait_for_timeout(600)
        await pg.screenshot(path=os.path.join(A,'og-image.png'))
        await b.close()
asyncio.run(main())
