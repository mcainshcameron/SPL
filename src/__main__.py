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

from .pipeline import (
    SPLProcessor,
    PlayerSummarizer,
    MarketCalculator,
    FantasyProcessor,
    NewsGenerator
)
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
    
    Processes Excel input and generates JSON files:
    - games.json
    - players.json
    - market_values.json
    - fantasy.json
    - news.json
    """
    try:
        input_path = Path(args.input)
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting pipeline: {input_path} -> {output_dir}")
        
        # Step 1: Process games and calculate points
        logger.info("Step 1/5: Processing games and calculating points")
        processor = SPLProcessor()
        games_df, points_df = processor.process_file(input_path)
        
        # Step 2: Generate player summaries
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
        fantasy_file = input_path.parent / "FantaSquadre" / f"FantaSquadre_{input_path.stem.split('_')[1]}.xlsx"
        fantasy_processor = FantasyProcessor()
        fantasy_data = fantasy_processor.process_fantasy_league(
            fantasy_file,
            points_df,
            season=args.fantasy_season
        )
        
        # Step 5: Generate news
        logger.info("Step 5/5: Generating SPLNews")
        news_gen = NewsGenerator()
        news_items = news_gen.generate_news(weekly_values, summaries)
        
        # Generate player name mappings
        all_players = points_df['Player'].unique().tolist()
        player_name_map = generate_player_names(all_players)
        player_name_map = ensure_unique_slugs(player_name_map)
        
        # Convert DataFrames to JSON-friendly formats
        logger.info("Converting data to JSON")
        
        # Games JSON
        games_json = games_df.to_dict(orient='records')
        for game in games_json:
            if 'Date' in game:
                game['Date'] = game['Date'].isoformat() if hasattr(game['Date'], 'isoformat') else str(game['Date'])
        
        # Players JSON (with display names and slugs)
        players_json = {}
        for champ, summary_df in summaries.items():
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
            
            players_json[champ] = players_list
        
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
    pipeline_parser.add_argument(
        '--input',
        required=True,
        help='Path to input Excel file'
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
