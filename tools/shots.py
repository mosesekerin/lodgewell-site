import asyncio, os, sys
from playwright.async_api import async_playwright
SP='/tmp/claude-0/-home-claude/099aa447-b20f-5ba7-88af-b8d897598eea/scratchpad/shots'; os.makedirs(SP,exist_ok=True)
F='/tmp/claude-0/-home-claude/099aa447-b20f-5ba7-88af-b8d897598eea/scratchpad/fontpkg'
FACES=''.join(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url(file://{F}/fontsource-{pk}-5.1.0/files/{pk}-latin-{w}-{st}.woff2)}}"
  for fam,pk,ws in [('Newsreader','newsreader',[500,600,700]),('Manrope','manrope',[400,500,600,700,800])] for w in ws for st in (['normal','italic'] if pk=='newsreader' else ['normal']))
URL='file://'+os.path.abspath('index.html')
async def shot(b,name,w,h,hash_,actions=None,full=False):
    pg=await b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/css',body=FACES))
    await pg.goto(URL+hash_); await pg.wait_for_timeout(500)
    if actions: await actions(pg); await pg.wait_for_timeout(400)
    await pg.screenshot(path=f'{SP}/{name}.png',full_page=full); print(name,'errors:',errs); await pg.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        await shot(b,'home-phone',390,844,'#/',full=True)
        await shot(b,'home-desk',1280,860,'#/')
        await shot(b,'q1-phone',390,844,'#/find/1')
        async def pick(pg):
            await pg.click('#f-body .opt[data-v="male"]'); await pg.click('#f-body .opt[data-v="2"]'); await pg.click('#f-body .opt[data-v="selfcon"]'); await pg.click('text=Next question')
        await shot(b,'q4-phone',390,844,'#/find/1',pick,full=True)
        async def finish(pg):
            await pg.click('#f-body .opt[data-v="male"]'); await pg.click('#f-body .opt[data-v="2"]'); await pg.click('#f-body .opt[data-v="selfcon"]'); await pg.click('text=Next question')
            await pg.click('#f-body .opt[data-v="Campus Gate"]'); await pg.click('#f-body .opt[data-v="Oduduwa Estate"]'); await pg.click('text=Next question')
            await pg.click('#f-body .opt[data-v="2"]'); await pg.click('text=/Show my/')
        await shot(b,'results-phone',390,1400,'#/find/1',finish,full=False)
        await shot(b,'results-desk',1280,1000,'#/find/1',finish)
        await b.close()
asyncio.run(main())
