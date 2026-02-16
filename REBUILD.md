# SPL v2 Site Rebuild Instructions

## Quick Rebuild

When you have updated data in `output/data/`, rebuild the site:

```bash
cd /data/.openclaw/workspace/spl-platform
python3 src/site/builder.py
```

The site will be regenerated in `output/site/` and is ready to deploy.

## What Gets Rebuilt

- All 6 main pages (home, classifica, mercato, fantalega, risultati)
- All 155 player profile pages
- Static assets are copied fresh

## Data Sources

The builder reads from these JSON files in `output/data/`:
- `games.json` - Game results
- `players.json` - Player statistics
- `market_values.json` - Market value history
- `fantasy.json` - Fantasy league data
- `news.json` - SPLNews headlines
- `player_names.json` - Name mappings

## Dependencies

- Python 3.11+
- Jinja2 (already installed on this system)

## Build Time

~5 seconds for complete rebuild

## Preview Locally

```bash
cd output/site
python3 -m http.server 8000
# Visit http://localhost:8000
```

## Deploy

Copy the entire `output/site/` directory to your web server or push to gh-pages branch.

## Troubleshooting

**Error: ModuleNotFoundError: No module named 'jinja2'**
```bash
python3 -m pip install jinja2
```

**Error: FileNotFoundError for data files**
- Ensure you're running from the spl-platform root directory
- Check that `output/data/*.json` files exist
- Run the data pipeline first if needed

**Missing logo**
- Ensure `src/static/images/logo.png` exists
- Or update the logo path in templates

## Customization

### Change Colors
Edit `src/static/css/styles.css` - all colors are defined as CSS custom properties at the top

### Add Pages
1. Create new template in `src/templates/`
2. Add build function in `src/site/builder.py`
3. Call it from `build_site()`

### Modify Layout
Edit templates in `src/templates/`:
- `base.html` - Navigation and layout
- `home.html` - Home page content
- etc.

### Add JavaScript
Add new JS files to `src/static/js/` and include in templates with:
```html
<script src="/static/js/your-file.js"></script>
```
