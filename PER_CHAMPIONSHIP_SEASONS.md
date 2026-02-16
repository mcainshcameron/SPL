# Per-Championship Season Numbering

## Overview

Each championship in the SPL platform maintains its own independent season counter starting from 1, regardless of when it started in calendar time.

## Implementation

The per-championship season renumbering is implemented in `src/pipeline/processor.py` in the `_process_games()` method:

```python
# Per-championship season renumbering (each championship starts from Season 1)
for champ in df['Championship'].unique():
    mask = df['Championship'] == champ
    champ_seasons = sorted(df.loc[mask, 'Season'].dropna().unique())
    if champ_seasons:
        season_map = {old: new + 1 for new, old in enumerate(champ_seasons)}
        df.loc[mask, 'Season'] = df.loc[mask, 'Season'].map(season_map)
```

### How It Works

1. **Global season calculation**: First, all games get a global season number based on the calendar date (Sep 1 → Jul 30 season boundaries)
2. **Championship split**: Games are assigned to their championship (Bovisa/Lambrate)
3. **Per-championship renumbering**: Within each championship, seasons are renumbered starting from 1

## Results

### Supabase Mode (as of 2026-02-16)

```
Bovisa:
  Seasons: [1, 2, 3, 4]
  Dates: 2023-01-12 to 2026-02-12
  Games: 114

Lambrate:
  Seasons: [1, 2]
  Dates: 2024-11-25 to 2025-11-18
  Games: 20
```

### Excel Mode (as of 2026-02-16)

```
Bovisa:
  Seasons: [1, 2, 3]
  Dates: 2023-01-12 to 2025-07-24
  Games: 101

Lambrate:
  Seasons: [1]
  Dates: 2024-11-25 to 2025-06-27
  Games: 17
```

## Why This Matters

Without per-championship renumbering, Lambrate (which started in late 2024) would show up as "Season 3" because it started during what would be the global "Season 3" timeframe.

With per-championship renumbering:
- **Bovisa** shows Stagione 1, 2, 3, 4 (started 2023)
- **Lambrate** shows Stagione 1, 2 (started 2024)
- **Combinata** shows Stagione 1, 2 (overlap period)

This makes sense from a user perspective - each venue has its own history and should count its own seasons from 1.

## Log Output

When running the pipeline, you'll see a log message confirming the per-championship season ranges:

```
INFO - Per-championship seasons: {'Bovisa': {'min': 1, 'max': 4}, 'Lambrate': {'min': 1, 'max': 2}}
```

## Applies to Both Modes

This fix works identically in both Excel mode (`--input`) and Supabase mode (`--supabase`), as both use the same `_process_games()` method in the processor.
