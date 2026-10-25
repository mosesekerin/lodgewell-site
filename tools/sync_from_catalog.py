"""Turn a private-catalog export into the public data/listings.json.

Usage: python3 tools/sync_from_catalog.py <export_dir> <your_charge_naira>
<export_dir>/listings/*.json are the raw catalog rows (never committed).
Only client-safe fields are written: no agent names, notes, search phrases or original prices.
"""
import json, glob, os, re, sys, datetime
src, charge = sys.argv[1], int(sys.argv[2])
KEEP = re.compile(r'^(gender|sharing|occupancy|arrangement|location|move-in|duration|water|toilet|kitchen|preference|units|walk)', re.I)
UNCLEAR = re.compile(r'not stated|confirm if rent or total', re.I)
def ref(i):
    m = re.match(r'^tm0*(\d+)$', i); return 'LW-' + (m.group(1).zfill(3) if m else i[-4:].upper())
items = []
for f in sorted(glob.glob(os.path.join(src, 'listings', '*.json'))):
    i = os.path.basename(f)[:-5]; r = json.load(open(f))
    if r.get('status') == 'taken' or r.get('example'): continue
    tp, rent = r.get('totalPackage'), r.get('rent')
    it = dict(ref=ref(i), type=r.get('type') or 'Apartment', area=r.get('area') or '', address=r.get('address'),
              features=r.get('features') or [], extra=[[k, v] for k, v in (r.get('extra') or {}).items() if KEEP.match(k)],
              seen=r.get('lastSeen') or r.get('added'), rep=r.get('reposts') or 0)
    if UNCLEAR.search(r.get('priceNote') or ''):
        base = tp if tp is not None else rent
        it['guide'] = (base + charge) if (tp is not None and base is not None) else base
    else:
        it['total'] = tp + charge if tp is not None else None
        it['rent'] = rent
    items.append(it)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'listings.json')
json.dump({'items': items, 'updated': datetime.datetime.now(datetime.timezone.utc).isoformat()}, open(out, 'w'), ensure_ascii=False, indent=1)
print(f'{len(items)} apartments written to data/listings.json')
