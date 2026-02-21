"""
SPL Supabase Loader
Loads game data from Supabase instead of Excel.
Transforms Supabase data to match Excel DataFrame structure.
"""

import logging
import os
from datetime import datetime
from typing import Dict, Tuple
import pandas as pd

from .config import SCORING_PARAMETERS

logger = logging.getLogger(__name__)

# Supabase connection config
SUPABASE_URL = "https://oejzratlwzwsrxoddhlp.supabase.co"


def get_supabase_key() -> str:
    """Get Supabase API key from environment."""
    key = os.environ.get("SPL_SUPABASE_KEY", "")
    if not key:
        raise ValueError("SPL_SUPABASE_KEY environment variable not set")
    return key


def _request(method: str, path: str, params: dict = None):
    """Make a request to Supabase REST API."""
    import json
    import urllib.request
    import urllib.parse
    
    key = get_supabase_key()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    
    req = urllib.request.Request(url, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_all(table: str, select: str = "*", order: str = None) -> list:
    """
    Fetch all rows from a table, handling pagination.
    Supabase caps at 1000 rows per request.
    """
    all_rows = []
    page_size = 1000
    offset = 0
    
    while True:
        params = {
            "select": select,
            "limit": str(page_size),
            "offset": str(offset)
        }
        if order:
            params["order"] = order
        
        rows = _request("GET", table, params=params)
        all_rows.extend(rows)
        
        if len(rows) < page_size:
            break
        offset += page_size
    
    return all_rows


def load_from_supabase() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict]:
    """
    Load data from Supabase and transform to Excel-equivalent DataFrames.
    
    Returns:
        Tuple of (games_df, points_df, players_df, parameters_dict)
        
        games_df columns: Date, Championship, Team A Goals, Team B Goals, Number of Players
        points_df columns: Date, Championship, Player, Team, Goals, Own Goals, SPL Bonus, 
                          MVP, Friend Referrals, Penalty, Game Position
        players_df columns: Player, Default 5 Position, Default 7 Position, Default 11 Position
        parameters_dict: scoring parameters by match type
    """
    logger.info("Loading data from Supabase")
    
    # Fetch all data
    logger.info("Fetching games")
    games = get_all("games", select="*", order="game_date.asc")
    
    logger.info("Fetching players")
    players = get_all("players", select="*")
    
    logger.info("Fetching player_game_stats")
    player_game_stats = get_all("player_game_stats", select="*")
    
    logger.info("Fetching game_formats")
    game_formats = get_all("game_formats", select="*")
    
    logger.info("Fetching positions")
    positions = get_all("positions", select="*")
    
    logger.info(f"Loaded: {len(games)} games, {len(players)} players, "
                f"{len(player_game_stats)} stats records, {len(game_formats)} formats, "
                f"{len(positions)} positions")
    
    # Build lookup dictionaries
    player_lookup = {p['id']: p for p in players}
    format_lookup = {f['id']: f for f in game_formats}
    position_lookup = {pos['id']: pos for pos in positions}
    
    # Transform games data
    games_data = []
    for game in games:
        # Count players in this game
        game_stats = [s for s in player_game_stats if s['game_id'] == game['id']]
        num_players = len(game_stats)
        
        games_data.append({
            'Date': pd.to_datetime(game['game_date']),
            'Championship': game.get('championship') or 'Bovisa',  # Default to Bovisa if null
            'Team A Goals': game['team_a_goals'] or 0,
            'Team B Goals': game['team_b_goals'] or 0,
            'Number of Players': num_players
        })
    
    games_df = pd.DataFrame(games_data)
    
    # Transform points data
    points_data = []
    for stat in player_game_stats:
        # Find the game
        game = next((g for g in games if g['id'] == stat['game_id']), None)
        if not game:
            logger.warning(f"Game {stat['game_id']} not found for stat {stat['id']}")
            continue
        
        # Find the player
        player = player_lookup.get(stat['player_id'])
        if not player:
            logger.warning(f"Player {stat['player_id']} not found for stat {stat['id']}")
            continue
        
        # Resolve game position
        game_position = None
        if stat.get('game_position_id'):
            pos = position_lookup.get(stat['game_position_id'])
            if pos:
                game_position = pos['name']
        
        points_data.append({
            'Date': pd.to_datetime(game['game_date']),
            'Championship': game.get('championship') or 'Bovisa',
            'Player': player['display_name'],  # Use display_name as the primary identifier
            'Team': stat['team'] if stat['team'] in ('Team A', 'Team B') else ('Team A' if stat['team'] == 'A' else 'Team B'),
            'Goals': stat.get('goals') or 0,
            'Own Goals': stat.get('own_goals') or 0,
            'SPL Bonus': stat.get('spl_bonus') or 0,
            'MVP': stat.get('mvp') or 0,
            'Friend Referrals': stat.get('friend_referrals') or 0,
            'Penalty': stat.get('penalty') or 0,
            'Game Position': game_position or ''
        })
    
    points_df = pd.DataFrame(points_data)
    
    # Transform players data
    players_data = []
    for player in players:
        # Resolve default positions
        default_5 = None
        default_7 = None
        default_11 = None
        
        if player.get('position_5_a_side_id'):
            pos = position_lookup.get(player['position_5_a_side_id'])
            if pos:
                default_5 = pos['name']
        
        if player.get('position_7_a_side_id'):
            pos = position_lookup.get(player['position_7_a_side_id'])
            if pos:
                default_7 = pos['name']
        
        if player.get('position_11_a_side_id'):
            pos = position_lookup.get(player['position_11_a_side_id'])
            if pos:
                default_11 = pos['name']
        
        players_data.append({
            'Player': player['display_name'],
            'Default 5 Position': default_5 or '',
            'Default 7 Position': default_7 or '',
            'Default 11 Position': default_11 or ''
        })
    
    players_df = pd.DataFrame(players_data)
    
    # Return scoring parameters from config
    parameters_dict = {'match_parameters': SCORING_PARAMETERS.parameters}
    
    logger.info(f"Transformed: {len(games_df)} games, {len(points_df)} points records, "
                f"{len(players_df)} players")
    
    return games_df, points_df, players_df, parameters_dict


def load_fantasy_from_supabase() -> Tuple[list, list]:
    """
    Load fantasy teams and rosters from Supabase.
    
    Returns:
        Tuple of (teams, rosters) where:
        - teams: list of dicts with id, team_name, owner_name
        - rosters: list of dicts with team_id, player_display_name, tier, price_millions
    """
    logger.info("Loading fantasy data from Supabase")
    
    teams = get_all("fantasy_teams", select="*", order="team_name.asc")
    rosters = get_all("fantasy_rosters", select="*")
    players = get_all("players", select="id,display_name")
    
    player_lookup = {p['id']: p['display_name'] for p in players}
    
    # Enrich rosters with player display names
    for r in rosters:
        r['player_display_name'] = player_lookup.get(r['player_id'], 'Unknown')
    
    logger.info(f"Loaded {len(teams)} fantasy teams, {len(rosters)} roster entries")
    
    return teams, rosters
