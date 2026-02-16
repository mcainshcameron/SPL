"""
SPL Platform CLI
Main entrypoint for pipeline and site building.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

from .pipeline import (
    SPLProcessor,
    PlayerSummarizer,
    MarketCalculator,
    FantasyProcessor,
    NewsGenerator
)
from .pipeline.supabase_loader import load_from_supabase
from .site.slugs import generate_player_names, ensure_unique_slugs


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_pipeline(args: argparse.Namespace) -> int:
    """
    Run the full data pipeline.
    
    Processes Excel input or Supabase data and generates JSON files:
    - games.json
    - players.json
    - market_values.json
    - fantasy.json
    - news.json
    """
    try:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Process games and calculate points
        logger.info("Step 1/5: Processing games and calculating points")
        processor = SPLProcessor()
        
        if args.supabase:
            # Supabase mode
            logger.info("Loading data from Supabase")
            games_df_raw, points_df_raw, players_df_raw, parameters_dict = load_from_supabase()
            games_df, points_df = processor.process_dataframes(
                games_df_raw, 
                points_df_raw, 
                players_df_raw, 
                parameters_dict
            )
            input_path = None  # No input file in Supabase mode
        else:
            # Excel mode
            input_path = Path(args.input)
            logger.info(f"Starting pipeline: {input_path} -> {output_dir}")
            games_df, points_df = processor.process_file(input_path)
        
        # Step 2: Generate player summaries (total and per-season)
        logger.info("Step 2/5: Generating player summaries")
        summarizer = PlayerSummarizer()
        summaries = summarizer.generate_summaries(points_df, games_df)
        season_summaries = summarizer.generate_season_summaries(points_df, games_df)
        
        # Step 3: Calculate market values
        logger.info("Step 3/5: Calculating market values")
        market_calc = MarketCalculator()
        weekly_values = market_calc.calculate_weekly_values(points_df)
        weekly_values = market_calc.calculate_value_changes(weekly_values)
        
        # Step 4: Process fantasy league (if file exists)
        logger.info("Step 4/5: Processing fantasy league")
        fantasy_processor = FantasyProcessor()
        
        if args.supabase:
            # Supabase mode: skip fantasy data (not in DB)
            logger.info("Supabase mode: skipping fantasy league (not in database)")
            fantasy_data = {
                'standings': pd.DataFrame(),
                'teams': pd.DataFrame()
            }
        else:
            # Excel mode: try to load fantasy data
            fantasy_file = input_path.parent / "FantaSquadre" / f"FantaSquadre_{input_path.stem.split('_')[1]}.xlsx"
            fantasy_data = fantasy_processor.process_fantasy_league(
                fantasy_file,
                points_df,
                season=args.fantasy_season
            )
        
        # Generate player name mappings (before news, so news can use display names)
        all_players = points_df['Player'].unique().tolist()
        player_name_map = generate_player_names(all_players)
        player_name_map = ensure_unique_slugs(player_name_map)
        
        # Step 5: Generate news
        logger.info("Step 5/5: Generating SPLNews")
        news_gen = NewsGenerator()
        news_items = news_gen.generate_news(weekly_values, summaries, player_name_map)
        
        # Convert DataFrames to JSON-friendly formats
        logger.info("Converting data to JSON")
        
        # Games JSON - Enrich with team compositions
        games_json = games_df.to_dict(orient='records')
        for game in games_json:
            if 'Date' in game:
                game['Date'] = game['Date'].isoformat() if hasattr(game['Date'], 'isoformat') else str(game['Date'])
            
            # Extract team compositions from points_df
            game_date = game.get('Date')
            game_champ = game.get('Championship')
            
            # Find all players from this game
            game_players = points_df[
                (points_df['Date'].astype(str).str[:10] == str(game_date)[:10]) &
                (points_df['Championship'] == game_champ)
            ]
            
            if not game_players.empty:
                # Group by team
                team_a_players = []
                team_b_players = []
                
                for _, player_row in game_players.iterrows():
                    player_name = player_row['Player']
                    team = player_row.get('Team', 'Team A')
                    goals = player_row.get('Goals', 0)
                    
                    # Get display name and slug
                    if player_name in player_name_map:
                        display_name = player_name_map[player_name]['display_name']
                        slug = player_name_map[player_name]['slug']
                    else:
                        display_name = player_name
                        slug = player_name.lower().replace(' ', '-')
                    
                    player_data = {
                        'name': display_name,
                        'slug': slug,
                        'goals': int(goals) if pd.notna(goals) else 0
                    }
                    
                    if team == 'Team A':
                        team_a_players.append(player_data)
                    else:
                        team_b_players.append(player_data)
                
                # Add to game
                game['team_a_players'] = sorted(team_a_players, key=lambda x: x['goals'], reverse=True)
                game['team_b_players'] = sorted(team_b_players, key=lambda x: x['goals'], reverse=True)
        
        # Players JSON - Restructure to championship -> season -> players
        # season_summaries has structure: {season: {championship: df}}
        # We want: {championship: {season: players_list}}
        players_json = {}
        
        # Championship name mapping (English -> Italian)
        champ_name_map = {
            'Combined': 'Combinata',
            'Bovisa': 'Bovisa',
            'Lambrate': 'Lambrate'
        }
        
        # Season name mapping (English -> Italian)
        def season_to_italian(season_key):
            if season_key == 'Total':
                return 'Totale'
            elif season_key.startswith('Season '):
                season_num = season_key.split()[1]
                return f'Stagione {season_num}'
            return season_key
        
        # Get all championships from total summaries
        championships = list(summaries.keys())
        
        for champ in championships:
            # Map championship name to Italian
            italian_champ = champ_name_map.get(champ, champ)
            players_json[italian_champ] = {}
            
            # Add all seasons for this championship
            for season_key, season_data in season_summaries.items():
                if champ in season_data:
                    italian_season = season_to_italian(season_key)
                    summary_df = season_data[champ]
                    players_list = []
                    
                    for _, row in summary_df.iterrows():
                        player_data = row.to_dict()
                        full_name = player_data['Player']
                        
                        # Add display name and slug
                        if full_name in player_name_map:
                            player_data['display_name'] = player_name_map[full_name]['display_name']
                            player_data['slug'] = player_name_map[full_name]['slug']
                        else:
                            player_data['display_name'] = full_name
                            player_data['slug'] = full_name.lower().replace(' ', '-')
                        
                        players_list.append(player_data)
                    
                    players_json[italian_champ][italian_season] = players_list
        
        # Market values JSON
        market_json = []
        for _, row in weekly_values.iterrows():
            market_data = row.to_dict()
            
            # Convert Week period to string
            if 'Week' in market_data:
                market_data['Week'] = str(market_data['Week'])
            
            # Add display name
            full_name = market_data['Player']
            if full_name in player_name_map:
                market_data['display_name'] = player_name_map[full_name]['display_name']
                market_data['slug'] = player_name_map[full_name]['slug']
            
            market_json.append(market_data)
        
        # Fantasy JSON
        fantasy_json = {
            'standings': fantasy_data['standings'].to_dict(orient='records'),
            'teams': fantasy_data['teams'].to_dict(orient='records')
        }
        
        # News JSON
        news_json = news_items
        
        # Save all JSON files
        logger.info(f"Saving JSON files to {output_dir}")
        
        with open(output_dir / 'games.json', 'w', encoding='utf-8') as f:
            json.dump(games_json, f, ensure_ascii=False, indent=2)
        
        with open(output_dir / 'players.json', 'w', encoding='utf-8') as f:
            json.dump(players_json, f, ensure_ascii=False, indent=2)
        
        with open(output_dir / 'market_values.json', 'w', encoding='utf-8') as f:
            json.dump(market_json, f, ensure_ascii=False, indent=2)
        
        with open(output_dir / 'fantasy.json', 'w', encoding='utf-8') as f:
            json.dump(fantasy_json, f, ensure_ascii=False, indent=2)
        
        with open(output_dir / 'news.json', 'w', encoding='utf-8') as f:
            json.dump(news_json, f, ensure_ascii=False, indent=2)
        
        with open(output_dir / 'player_names.json', 'w', encoding='utf-8') as f:
            json.dump(player_name_map, f, ensure_ascii=False, indent=2)
        
        logger.info("Pipeline complete!")
        logger.info(f"Generated files:")
        logger.info(f"  - games.json ({len(games_json)} games)")
        logger.info(f"  - players.json ({sum(len(p) for p in players_json.values())} player entries)")
        logger.info(f"  - market_values.json ({len(market_json)} value records)")
        logger.info(f"  - fantasy.json ({len(fantasy_json['standings'])} teams)")
        logger.info(f"  - news.json ({len(news_json)} headlines)")
        logger.info(f"  - player_names.json ({len(player_name_map)} players)")
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return 1


def run_build(args: argparse.Namespace) -> int:
    """Build static site from processed JSON data."""
    logger.info("Site building not yet implemented")
    logger.info("This will be implemented in Phase 3")
    return 0


def main() -> int:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description='SPL Platform - Data pipeline and site builder'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Pipeline command
    pipeline_parser = subparsers.add_parser('pipeline', help='Run data pipeline')
    
    # Data source: either --input (Excel) or --supabase (database)
    source_group = pipeline_parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        '--input',
        help='Path to input Excel file'
    )
    source_group.add_argument(
        '--supabase',
        action='store_true',
        help='Load data from Supabase instead of Excel'
    )
    
    pipeline_parser.add_argument(
        '--output',
        default='output/data',
        help='Output directory for JSON files (default: output/data)'
    )
    pipeline_parser.add_argument(
        '--fantasy-season',
        type=int,
        default=None,
        help='Fantasy league season to process (default: all seasons)'
    )
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build static site')
    build_parser.add_argument(
        '--data',
        default='output/data',
        help='Input directory with JSON files (default: output/data)'
    )
    build_parser.add_argument(
        '--output',
        default='output/site',
        help='Output directory for static site (default: output/site)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'pipeline':
        return run_pipeline(args)
    elif args.command == 'build':
        return run_build(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
