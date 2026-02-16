#!/usr/bin/env python3
"""
SPL v2 Static Site Builder
Reads processed JSON data and generates complete static HTML site.
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "output" / "data"
TEMPLATES_DIR = BASE_DIR / "src" / "templates"
STATIC_DIR = BASE_DIR / "src" / "static"
OUTPUT_DIR = BASE_DIR / "output" / "site"


def load_data():
    """Load all JSON data files"""
    print("Loading data...")
    with open(DATA_DIR / "games.json") as f:
        games = json.load(f)
    with open(DATA_DIR / "players.json") as f:
        players = json.load(f)
    with open(DATA_DIR / "market_values.json") as f:
        market_values = json.load(f)
    with open(DATA_DIR / "fantasy.json") as f:
        fantasy = json.load(f)
    with open(DATA_DIR / "news.json") as f:
        news = json.load(f)
    with open(DATA_DIR / "player_names.json") as f:
        player_names = json.load(f)
    
    return {
        "games": games,
        "players": players,
        "market_values": market_values,
        "fantasy": fantasy,
        "news": news,
        "player_names": player_names
    }


def format_currency(value):
    """Format value as €X.XM"""
    if value >= 1_000_000:
        return f"€{value / 1_000_000:.1f}M"
    return f"€{value / 1000:.0f}K"


def format_change(value):
    """Format value change with sign"""
    if value > 0:
        return f"+{format_currency(value)}"
    elif value < 0:
        return format_currency(value)
    return "—"


def format_percent(value):
    """Format as percentage"""
    return f"{value:.1f}%"


def get_player_market_history(player_name, market_values):
    """Get full market history for a player"""
    history = [mv for mv in market_values if mv["Player"] == player_name]
    history.sort(key=lambda x: x["Week"])
    return history


def get_latest_market_value(player_name, market_values):
    """Get latest market value for a player"""
    history = get_player_market_history(player_name, market_values)
    if history:
        return history[-1]
    return None


def get_player_stats_by_season(player_name, games):
    """Get player stats broken down by season from games data"""
    player_games = [g for g in games if player_name in str(g)]
    # This is simplified - would need actual points data with player info
    # For now, return empty - real implementation would parse from detailed game data
    return {}


def get_recent_games(games, championship=None, limit=5):
    """Get most recent games, optionally filtered by championship"""
    filtered = games if not championship else [g for g in games if g["Championship"] == championship]
    sorted_games = sorted(filtered, key=lambda x: x["Date"], reverse=True)
    return sorted_games[:limit]


def get_top_performers(players_data, championship=None):
    """Get top performers from rankings"""
    # Players data now has structure: {championship: {season: players}}
    # Always use "Totale" season for top performers
    if championship and championship in players_data:
        data = players_data[championship].get("Totale", [])
    elif "Combinata" in players_data:
        data = players_data["Combinata"].get("Totale", [])
    else:
        # Use first available championship's Totale
        first_champ = list(players_data.values())[0]
        data = first_champ.get("Totale", [])
    
    # Return top 10 by PPG
    sorted_players = sorted(data, key=lambda x: x.get("PPG", 0), reverse=True)
    return sorted_players[:10]


def build_home_page(env, data):
    """Build home page"""
    print("Building home page...")
    template = env.get_template("home.html")
    
    # Get recent games per championship
    championships = set(g["Championship"] for g in data["games"])
    recent_by_champ = {
        champ: get_recent_games(data["games"], champ, 1)[0] if get_recent_games(data["games"], champ, 1) else None
        for champ in championships
    }
    
    # Quick stats
    total_games = len(data["games"])
    
    # Top performer (highest PPG from Combined)
    top_performers = get_top_performers(data["players"])
    top_performer = top_performers[0] if top_performers else None
    
    html = template.render(
        news=data["news"][:10],  # Latest 10 headlines
        recent_games=recent_by_champ,
        total_games=total_games,
        top_performer=top_performer,
        championships=sorted(championships)
    )
    
    output_file = OUTPUT_DIR / "index.html"
    output_file.write_text(html)
    print(f"  ✓ {output_file}")


def build_classifica_page(env, data):
    """Build rankings page"""
    print("Building classifica page...")
    template = env.get_template("classifica.html")
    
    # Players data now has structure: {championship: {season: players}}
    # Pass the full nested structure
    championships_data = data["players"]
    
    # Sort players within each season by Rank
    for champ in championships_data:
        for season in championships_data[champ]:
            championships_data[champ][season] = sorted(
                championships_data[champ][season], 
                key=lambda x: x["Rank"]
            )
    
    html = template.render(
        championships=championships_data
    )
    
    output_file = OUTPUT_DIR / "classifica" / "index.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html)
    print(f"  ✓ {output_file}")


def build_mercato_page(env, data):
    """Build market page"""
    print("Building mercato page...")
    template = env.get_template("mercato.html")
    
    # Get all unique players from Combinata Totale
    all_players = set()
    if "Combinata" in data["players"] and "Totale" in data["players"]["Combinata"]:
        for p in data["players"]["Combinata"]["Totale"]:
            all_players.add(p["Player"])
    
    # Get latest market values per player
    latest_values = {}
    for player in data["player_names"].values():
        player_name = player["full_name"]
        if player_name not in all_players:
            continue
            
        mv = get_latest_market_value(player_name, data["market_values"])
        if mv:
            latest_values[player["slug"]] = {
                "display_name": player["display_name"],
                "slug": player["slug"],
                "value": mv["Market Value"],
                "change": mv.get("Value Change", 0),
                "change_percent": mv.get("Value Change %", 0),
                "history": get_player_market_history(player_name, data["market_values"])[-10:]  # Last 10 weeks
            }
    
    # Sort by value
    sorted_players = sorted(latest_values.values(), key=lambda x: x["value"], reverse=True)
    
    html = template.render(
        players=sorted_players
    )
    
    output_file = OUTPUT_DIR / "mercato" / "index.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html)
    print(f"  ✓ {output_file}")


def build_player_pages(env, data):
    """Build individual player profile pages"""
    print("Building player pages...")
    template = env.get_template("player.html")
    
    for player_info in data["player_names"].values():
        player_name = player_info["full_name"]
        slug = player_info["slug"]
        
        # Get player stats from all championships (use "Totale" season)
        player_stats = {}
        for champ, seasons in data["players"].items():
            totale_players = seasons.get("Totale", [])
            for p in totale_players:
                if p["Player"] == player_name:
                    player_stats[champ] = p
                    break
        
        # Skip if player has no stats
        if not player_stats:
            continue
        
        # Get market history
        market_history = get_player_market_history(player_name, data["market_values"])
        latest_value = market_history[-1] if market_history else None
        
        # Get game log - simplified (would need detailed points data)
        # For now, just pass empty
        game_log = []
        
        html = template.render(
            player=player_info,
            stats=player_stats,
            market_history=market_history,
            latest_value=latest_value,
            game_log=game_log
        )
        
        output_file = OUTPUT_DIR / "players" / slug / "index.html"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html)
    
    print(f"  ✓ Built {len(data['player_names'])} player pages")


def build_fantalega_page(env, data):
    """Build fantasy league page"""
    print("Building fantalega page...")
    template = env.get_template("fantalega.html")
    
    # Import display name function
    from slugs import generate_display_name
    
    # Process standings to add owner display names
    standings_with_display = []
    for team in data["fantasy"]["standings"]:
        team_copy = team.copy()
        owner_full = team["Owner"]
        team_copy["owner_display"] = generate_display_name(owner_full)
        standings_with_display.append(team_copy)
    
    # Group teams data by team name
    teams_list = data["fantasy"].get("teams", [])
    rosters = {}
    for entry in teams_list:
        team_name = entry["Team Name"]
        if team_name not in rosters:
            rosters[team_name] = []
        
        # Find player info from player_names
        player_name = entry["Player"]
        player_info = data["player_names"].get(player_name, {
            "display_name": player_name,
            "slug": player_name.lower().replace(" ", "-")
        })
        rosters[team_name].append(player_info)
    
    html = template.render(
        standings=standings_with_display,
        rosters=rosters
    )
    
    output_file = OUTPUT_DIR / "fantalega" / "index.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html)
    print(f"  ✓ {output_file}")


def build_risultati_page(env, data):
    """Build game results page"""
    print("Building risultati page...")
    template = env.get_template("risultati.html")
    
    # Sort all games by date descending (newest first), as a flat list
    sorted_games = sorted(data["games"], key=lambda x: x["Date"], reverse=True)
    
    # Get unique championships and seasons for filters
    championships = sorted(set(g["Championship"] for g in data["games"]))
    seasons = sorted(set(g["Season"] for g in data["games"]))
    
    html = template.render(
        games=sorted_games,
        championships=championships,
        seasons=seasons
    )
    
    output_file = OUTPUT_DIR / "risultati" / "index.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html)
    print(f"  ✓ {output_file}")


def copy_static_assets():
    """Copy CSS, JS, images to output"""
    print("Copying static assets...")
    
    # Copy entire static directory
    output_static = OUTPUT_DIR / "static"
    if output_static.exists():
        shutil.rmtree(output_static)
    shutil.copytree(STATIC_DIR, output_static)
    print(f"  ✓ Copied static files")
    
    # Copy logo if exists
    logo_source = Path("/tmp/FantaSPL_code/HTML/Solo Pro League - SPL.png")
    if logo_source.exists():
        shutil.copy(logo_source, output_static / "images" / "logo.png")
        print(f"  ✓ Copied logo")


def build_site():
    """Main build function"""
    print("=" * 60)
    print("SPL v2 Static Site Builder")
    print("=" * 60)
    
    # Load data
    data = load_data()
    
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    env.filters["currency"] = format_currency
    env.filters["change"] = format_change
    env.filters["percent"] = format_percent
    
    # Clean output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Build all pages
    build_home_page(env, data)
    build_classifica_page(env, data)
    build_mercato_page(env, data)
    build_player_pages(env, data)
    build_fantalega_page(env, data)
    build_risultati_page(env, data)
    
    # Copy static assets
    copy_static_assets()
    
    print("=" * 60)
    print(f"✓ Site built successfully!")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: python -m http.server -d {OUTPUT_DIR} 8000")
    print("=" * 60)


if __name__ == "__main__":
    build_site()
