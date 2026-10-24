# Lodgewell Apartments

Public listings site for Lodgewell, a homes and lodges agency in Ile-Ife.
Clients search by type, budget, area, gender and sharing, then request an inspection on WhatsApp.

## How it works

- `data/listings.json`: the client-safe listings (prices already include Lodgewell's charge).
- `src/template.html` and `src/style.html`: the page.
- `build.py`: writes `index.html` from the two above. No dependencies beyond Python 3.
- `site.json`: site address, title and description used for link previews.
- `assets/`: logo, favicon and the link-preview image (`og-image.png`, 1200×630).

GitHub Pages serves `index.html` from the `main` branch.

## Updating

The private catalog (Agent view, original prices, agent sources) stays in Claude and never comes into this repo.
To update the site, Claude exports the catalog, runs:

```
python3 tools/sync_from_catalog.py <export_dir> <charge>
python3 build.py
```

then commits and pushes. GitHub Pages republishes within a minute or two.
