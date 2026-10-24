"""Build index.html from src/ + data/listings.json.  Usage: python3 build.py"""
import json, datetime, html, os
ROOT = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
site = json.loads(rd('site.json'))
snap = json.loads(rd('data/listings.json'))
items = snap['items']
base = site['url'].rstrip('/')
img = (base + '/' if base else '') + 'assets/og-image.png'
upd = datetime.datetime.fromisoformat(snap['updated'].replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=1)))
e = lambda s: html.escape(s, quote=True)
head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(site['title'])}</title>
<meta name="description" content="{e(site['description'])}">
<meta name="theme-color" content="#1F3D36">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
{f'<link rel="canonical" href="{e(base)}/">' if base else ''}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lodgewell">
<meta property="og:title" content="{e(site['title'])}">
<meta property="og:description" content="{e(site['description'])}">
<meta property="og:image" content="{e(img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
{f'<meta property="og:url" content="{e(base)}/">' if base else ''}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{e(img)}">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
'''
body = rd('src/template.html')
data = json.dumps(items, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
body = (body.replace('%%STYLE%%', rd('src/style.html'))
            .replace('%%DATA%%', data)
            .replace('%%UPDATED%%', upd.strftime('%-d %b %Y'))
            .replace('%%COUNT%%', str(len(items))))
first_style_end = body.index('</style>', body.index('</style>') + 1) + 8  # brand css + page css
out = head + body[:first_style_end] + '\n</head>\n<body>\n' + body[first_style_end:] + '\n</body>\n</html>\n'
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(out)
print(f'index.html built: {len(items)} apartments, updated {upd:%d %b %Y %H:%M}')
