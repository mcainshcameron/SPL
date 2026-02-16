#!/usr/bin/env python3
"""
Quick utility to inspect generated JSON files.
"""

import json
import sys
from pathlib import Path


def check_output(output_dir: Path = Path("output/data")):
    """Check all generated JSON files."""
    
    files = {
        'games.json': 'games',
        'players.json': 'player entries across championships',
        'market_values.json': 'market value records',
        'fantasy.json': 'fantasy teams',
        'news.json': 'news headlines',
        'player_names.json': 'player name mappings'
    }
    
    print(f"\n{'='*60}")
    print(f"SPL Pipeline Output Check")
    print(f"{'='*60}\n")
    
    for filename, description in files.items():
        filepath = output_dir / filename
        
        if not filepath.exists():
            print(f"❌ {filename}: NOT FOUND")
            continue
        
        # Get file size
        size = filepath.stat().st_size
        size_str = f"{size / 1024:.1f}KB" if size < 1_000_000 else f"{size / 1_000_000:.1f}MB"
        
        # Load and count
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            count = len(data)
        elif isinstance(data, dict):
            if 'standings' in data:  # Fantasy
                count = len(data['standings'])
            else:  # Players (nested dict)
                count = sum(len(v) for v in data.values() if isinstance(v, list))
        else:
            count = "?"
        
        print(f"✅ {filename:25} {size_str:>10}  |  {count} {description}")
    
    print(f"\n{'='*60}\n")
    
    # Show sample news headlines
    news_path = output_dir / 'news.json'
    if news_path.exists():
        with open(news_path, 'r') as f:
            news = json.load(f)
        
        print("📰 Sample News Headlines:\n")
        for item in news[:5]:
            print(f"  • {item['headline']}")
        print()
    
    # Show top players
    players_path = output_dir / 'players.json'
    if players_path.exists():
        with open(players_path, 'r') as f:
            players = json.load(f)
        
        combined = players.get('Combined', [])
        if combined:
            print("🏆 Top 5 Players (Combined):\n")
            for i, player in enumerate(combined[:5], 1):
                name = player.get('display_name', player.get('Player'))
                pts = player.get('Total Points', 0)
                games = player.get('Games Played', 0)
                ppg = player.get('PPG', 0)
                print(f"  {i}. {name:20} {pts:>6.0f} pts  |  {games} games  |  {ppg:.2f} PPG")
            print()


if __name__ == '__main__':
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/data")
    check_output(output_dir)
