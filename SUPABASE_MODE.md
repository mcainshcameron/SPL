# Supabase Data Source

The SPL v2 pipeline now supports loading data from Supabase in addition to Excel files.

## Usage

### Supabase Mode
```bash
python3 -m src pipeline --supabase --output output/data
```

### Excel Mode (existing)
```bash
python3 -m src pipeline --input data/input/file.xlsx --output output/data
```

## Environment Variables

Set the Supabase API key:
```bash
export SPL_SUPABASE_KEY="your_supabase_key_here"
```

## What Works

✅ Load games from Supabase `games` table
✅ Load players from Supabase `players` table
✅ Load game stats from `player_game_stats` table
✅ Resolve positions from `positions` table
✅ Resolve game formats from `game_formats` table
✅ Transform data to match Excel structure exactly
✅ Championship split (Bovisa/Lambrate/Combinata)
✅ Season calculation (Sep 1 → Jul 30)
✅ **Per-championship season numbering** - Each championship's seasons start from 1
✅ All point calculations work identically
✅ Market value calculations
✅ News generation
✅ Player name slugs

### Per-Championship Season Numbering

Each championship maintains its own season counter starting from 1, even if they overlap in calendar time:

- **Bovisa** (started 2023): Stagione 1, 2, 3, 4...
- **Lambrate** (started 2024): Stagione 1, 2...
- **Combinata** (overlap period): Stagione 1, 2...

This means Lambrate's first season is "Stagione 1" even though it chronologically overlaps with Bovisa's "Stagione 3". This makes sense from a user perspective - each venue has its own history.

## Differences from Excel Mode

- **Fantasy league**: Skipped in Supabase mode (fantasy data not in database)
- **Data source**: Reads from Supabase database instead of Excel file
- **Real-time**: Can access the latest data without manual Excel exports

## Database Schema

Tables used:
- `games`: id, game_date, team_a_goals, team_b_goals, game_format_id, championship, venue, notes
- `players`: id, player_code, display_name, full_name, position_*_a_side_id, is_active
- `player_game_stats`: id, game_id, player_id, team, goals, own_goals, spl_bonus, mvp, friend_referrals, penalty, game_position_id
- `game_formats`: id, name (5-a-side/7-a-side/11-a-side), description
- `positions`: id, name, position_category

## Scoring Parameters

Scoring parameters are now defined in `src/pipeline/config.py` as `SCORING_PARAMETERS`.
They match the Excel Parameters sheet exactly.

## Output Files

Both modes produce the same JSON files:
- `games.json` - All games with dates, scores, match types
- `players.json` - Player statistics by championship and season
- `market_values.json` - Weekly market valuations
- `news.json` - SPLNews headlines
- `player_names.json` - Display name and slug mappings
- `fantasy.json` - Fantasy league data (empty in Supabase mode)

## Implementation Files

New files:
- `src/pipeline/supabase_loader.py` - Supabase data loader

Modified files:
- `src/pipeline/config.py` - Added `SCORING_PARAMETERS`
- `src/pipeline/processor.py` - Added `process_dataframes()` method
- `src/__main__.py` - Added `--supabase` flag

## Testing

Both modes tested and working:
```bash
# Test Supabase mode
python3 -m src pipeline --supabase

# Test Excel mode
python3 -m src pipeline --input /path/to/file.xlsx

# Both produce compatible output
```
