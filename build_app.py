"""Build the interactive site (src/app.html) into <out>/index.html.  Usage: python3 build_app.py [outdir]  (default: . = the main site)"""
import json, datetime, html, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); out_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
site = json.loads(rd('site.json')); snap = json.loads(rd('data/listings.json')); items = snap['items']
base = site['url'].rstrip('/'); depth = '' if out_dir in ('', '.') else '../'
page_url = base + ('/' if depth == '' else f'/{out_dir}/')
img = base + '/assets/og-image.png'
e = lambda s: html.escape(s, quote=True)
MARK = ('<svg viewBox="0 0 64 64" aria-hidden="true"><defs><mask id="m{n}"><rect width="64" height="64" fill="#fff"/><circle cx="32" cy="43" r="3.2" fill="#000"/>'
        '<path d="M30.4 45 L29.4 51.5 H34.6 L33.6 45 Z" fill="#000"/></mask></defs><path d="M8 31 L32 10 L56 31" fill="none" stroke="#C8963E" stroke-width="5.5" stroke-linecap="square"/>'
        '<path d="M22 57 V41 A10 10 0 0 1 42 41 V57 Z" fill="#F7F3EC" mask="url(#m{n})"/><rect x="10" y="56" width="44" height="3" fill="#F7F3EC"/></svg>')
body = rd('src/app.html')
n = 0
while '%%MARK%%' in body:
    body = body.replace('%%MARK%%', MARK.format(n=n), 1); n += 1
data = json.dumps(items, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
body = body.replace('%%DATA%%', data).replace('%%UPDATED_ISO%%', json.dumps(snap['updated']))
split = body.index('</style>') + 8
head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(site['title'])}</title>
<meta name="description" content="{e(site['description'])}">
<meta name="theme-color" content="#1F3D36">
<link rel="icon" href="{depth}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{depth}assets/apple-touch-icon.png">
<link rel="canonical" href="{e(page_url)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Lodgewell">
<meta property="og:title" content="{e(site['title'])}"><meta property="og:description" content="{e(site['description'])}">
<meta property="og:image" content="{e(img)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="{e(page_url)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{e(img)}">
'''
out = head + body[:split] + '\n</head>\n<body>\n' + body[split:] + '\n</body>\n</html>\n'
d = os.path.join(ROOT, out_dir); os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
print(f'{"" if out_dir in (".","") else out_dir+"/"}index.html built: {len(items)} rooms')
