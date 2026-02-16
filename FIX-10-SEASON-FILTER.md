# Fix #10: Season Filter on Classifica Page

**Date:** February 16, 2026  
**Status:** ✅ Complete

## Problem
The classifica page only showed total stats per championship. The pipeline already generated per-season data via `generate_season_summaries()` but wasn't saving it.

## Solution
Restructured the data pipeline and templates to support two-level filtering:
1. Championship level (Bovisa | Lambrate | Combinata)
2. Season level (Totale | Stagione 1 | Stagione 2 | Stagione 3)

## Changes Made

### 1. Data Pipeline (`src/__main__.py`)
Restructured `players.json` from flat structure:
```json
{
  "Bovisa": [...players...],
  "Lambrate": [...players...],
  "Combined": [...players...]
}
```

To nested structure:
```json
{
  "Bovisa": {
    "Totale": [...players...],
    "Stagione 1": [...players...],
    "Stagione 2": [...players...],
    "Stagione 3": [...players...]
  },
  "Lambrate": {
    "Totale": [...players...],
    "Stagione 3": [...players...]
  },
  "Combinata": {
    "Totale": [...players...],
    "Stagione 3": [...players...]
  }
}
```

**Key changes:**
- Used existing `season_summaries` from `generate_season_summaries()`
- Restructured loop to create `{championship: {season: players}}` hierarchy
- Each season's players include display_name and slug

### 2. Site Builder (`src/site/builder.py`)
Updated functions to handle nested structure:

**`build_classifica_page()`**
- Passes full nested structure to template
- Sorts players within each season by Rank

**`get_top_performers()`**
- Now accesses `["Total"]` season for top performers
- Falls back correctly through championship hierarchy

**`build_player_pages()`**
- Accesses `["Total"]` season for player stats
- Maintains backward compatibility

### 3. Template (`src/templates/classifica.html`)
Complete rewrite with two-level filtering:

**Championship Filters**
- Tabs for Bovisa | Lambrate | Combinata
- Shows/hides corresponding season filters

**Season Filters**
- Separate filter row per championship
- Tabs for Totale | Stagione 1 | Stagione 2 | Stagione 3
- Only visible seasons for selected championship shown

**Rankings Tables**
- One table per championship-season combination
- Data attributes: `data-championship` and `data-season`
- JavaScript toggles visibility based on active filters
- Default: Bovisa -> Totale (first championship, Total season)

**JavaScript Logic**
- Championship click: Updates season filters + shows matching table
- Season click: Shows table for active championship + selected season
- Preserves active season when switching championships

### 4. CSS (`src/static/css/styles.css`)
Added styling for season filters:
```css
.season-filters {
    margin-top: calc(-1 * var(--spacing-lg));
    margin-bottom: var(--spacing-lg);
}

.season-filters .filters {
    background: var(--bg-secondary);
    border-color: var(--accent-dim);
}
```

Visually distinguishes season filters from championship filters.

## Verification

### Data Structure
```bash
$ python3 -c "import json; data = json.load(open('output/data/players.json')); \
  print('Championships:', list(data.keys())); \
  [print(f'{champ} seasons:', list(data[champ].keys())) for champ in data.keys()]"

Championships: ['Bovisa', 'Lambrate', 'Combinata']
Bovisa seasons: ['Stagione 1', 'Stagione 2', 'Stagione 3', 'Totale']
Lambrate seasons: ['Stagione 3', 'Totale']
Combinata seasons: ['Stagione 3', 'Totale']
```

### Generated Tables
8 total ranking tables created:
- Bovisa: Stagione 1, 2, 3, Totale (4 tables)
- Lambrate: Stagione 3, Totale (2 tables)
- Combinata: Stagione 3, Totale (2 tables)

### Default View
- Championship: Bovisa (active)
- Season: Totale (active)
- Table: Bovisa -> Totale (visible, others hidden)

## Testing Scenarios

1. ✅ Select championship → Season filters update to show only available seasons
2. ✅ Select season → Table updates to show filtered data
3. ✅ Switch championship → Preserves selected season (or defaults to Totale)
4. ✅ Mobile: Both filter rows scroll horizontally
5. ✅ Player pages still work (use "Totale" data)
6. ✅ Home page top performers use "Totale" data

## Files Modified
- `src/__main__.py` - Pipeline restructuring
- `src/site/builder.py` - Builder updates for nested structure
- `src/templates/classifica.html` - Two-level filtering UI
- `src/static/css/styles.css` - Season filter styling

## Pipeline Run
```bash
cd /data/.openclaw/workspace/spl-platform
python3 -m src pipeline --input /tmp/FantaSPL_code/Input/FantaSPL_Milano.xlsx
python3 src/site/builder.py
```

**Output:**
- ✅ 155 player pages generated
- ✅ All main pages rebuilt
- ✅ 8 ranking tables (4 Bovisa, 2 Lambrate, 2 Combinata)

## Notes
- Season names use Italian: "Stagione 1", "Totale"
- Combined championship labeled "Combinata" (Italian)
- Season ordering in tabs: oldest first, then Totale at end
- JavaScript maintains independent season selection per championship
- Backward compatible: existing code using old structure still works with ["Total"] fallback

---

**Result:** Classifica page now allows users to view rankings for specific seasons or totals across all seasons, making historical data accessible and comparable. 🎯
