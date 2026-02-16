# SPL Platform v2 - Quick Start

## Installation

```bash
cd /data/.openclaw/workspace/spl-platform
pip install -e . --break-system-packages
```

## Run Pipeline

```bash
# Full pipeline
python -m src pipeline --input data/input/FantaSPL_Milano.xlsx

# With custom output dir
python -m src pipeline --input data/input/FantaSPL_Milano.xlsx --output output/data

# Process specific fantasy season
python -m src pipeline --input data/input/FantaSPL_Milano.xlsx --fantasy-season 2
```

## Check Output

```bash
# Quick check of generated files
python3 scripts/check_output.py

# Check custom output dir
python3 scripts/check_output.py path/to/output
```

## Output Files

All JSON files are written to `output/data/`:

- **games.json** — All games with championship, season, gameweek
- **players.json** — Player summaries by championship
- **market_values.json** — Weekly market values with full history
- **fantasy.json** — Fantasy league standings and rosters
- **news.json** — Auto-generated Italian headlines
- **player_names.json** — Display names and URL slugs

## Testing with Real Data

The pipeline has been tested with the actual SPL Milano Excel file and successfully generated all outputs:

```
✅ 118 games processed
✅ 357 player entries (Bovisa: 138, Lambrate: 64, Combined: 155)
✅ 8,660 market value records (95 weeks)
✅ 40 fantasy teams
✅ 14 news headlines
✅ 155 player names mapped
```

## Next: Phase 3

Site builder (Jinja2 templates + static HTML/CSS/JS) — coming next!
