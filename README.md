# Lodgewell Apartments

Public listings site for Lodgewell, a homes and lodges agency in Ile-Ife.
Clients search by type, budget, area, gender and sharing, then request an inspection on WhatsApp.

## How it works

- `data/listings.json`: the client-safe listings (prices already include Lodgewell's charge).
- `src/app.html`: the site (landing page, 5-question finder, results).
- `build_app.py`: writes the main `index.html` from `src/app.html`. No dependencies beyond Python 3.
- `build.py`: writes the old catalog page to `old/index.html` (kept as a backup) from `src/template.html` and `src/style.html`.
- `new/index.html`: redirects the old preview address to the main site.
- `site.json`: site address, title and description used for link previews.
- `assets/`: logo, favicon and the link-preview image (`og-image.png`, 1200×630).

GitHub Pages serves `index.html` from the `main` branch.

## Updating

The private catalog (Agent view, original prices, agent sources) stays in Claude and never comes into this repo.
To update the site, Claude exports the catalog, runs:

```
python3 tools/sync_from_catalog.py <export_dir> <charge>
python3 build_app.py
python3 build.py
```

To roll back to the old catalog as the main page: `cp old/index.html index.html` and fix its `../assets` paths to `assets`.

then commits and pushes. GitHub Pages republishes within a minute or two.
