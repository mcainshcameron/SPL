"""
SPL Data Processor
Processes raw game data and calculates player points.
Ported from SPL_Processor_v0.4.py with improvements.
"""

import logging
import math
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd

from .config import calculate_season_from_date, CHAMPIONSHIP_CONFIG

logger = logging.getLogger(__name__)


class MatchType(Enum):
    """Match types based on number of players."""
    FIVE_A_SIDE = "5-a-side"
    SEVEN_A_SIDE = "7-a-side"
    ELEVEN_A_SIDE = "11-a-side"

    @classmethod
    def from_players(cls, num_players: int) -> 'MatchType':
        """Determine match type from number of players."""
        if num_players <= 10:
            return cls.FIVE_A_SIDE
        elif num_players < 17:
            return cls.SEVEN_A_SIDE
        else:
            return cls.ELEVEN_A_SIDE


class GameOutcome(Enum):
    """Game outcomes."""
    WIN = "Win"
    DRAW = "Draw"
    LOSS = "Loss"

    @classmethod
    def from_goal_diff(cls, goal_diff: int) -> 'GameOutcome':
        """Determine outcome from goal difference."""
        if goal_diff > 0:
            return cls.WIN
        elif goal_diff < 0:
            return cls.LOSS
        return cls.DRAW


class SPLProcessor:
    """Main processor for SPL game data."""
    
    def __init__(self) -> None:
        self.config: Optional[Dict] = None
        
    def process_file(self, input_path: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Process SPL data from Excel file.
        
        Args:
            input_path: Path to input Excel file
            
        Returns:
            Tuple of (games_df, points_df)
        """
        logger.info(f"Processing file: {input_path}")
        
        # Load all sheets
        data_frames = self._load_data(input_path)
        
        # Load configuration from Parameters sheet
        self._load_config(data_frames['Parameters'])
        
        # Preprocess and validate
        self._preprocess_data(data_frames)
        
        # Process games and calculate points
        games_df = self._process_games(data_frames['Games'], data_frames['Points'])
        points_df = self._calculate_points(
            data_frames['Points'],
            games_df,
            data_frames['Players']
        )
        
        logger.info(f"Processing complete: {len(games_df)} games, {len(points_df)} point records")
        return games_df, points_df
    
    def process_dataframes(
        self,
        games_df: pd.DataFrame,
        points_df: pd.DataFrame,
        players_df: pd.DataFrame,
        parameters_dict: Dict
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Process SPL data from pre-loaded DataFrames (e.g., from Supabase).
        
        Args:
            games_df: Games DataFrame with columns: Date, Championship, Team A Goals, Team B Goals
            points_df: Points DataFrame with columns: Date, Championship, Player, Team, Goals, etc.
            players_df: Players DataFrame with columns: Player, Default 5 Position, etc.
            parameters_dict: Scoring parameters dict with 'match_parameters' key
            
        Returns:
            Tuple of (games_df, points_df)
        """
        logger.info("Processing DataFrames")
        
        # Set configuration
        self.config = parameters_dict
        
        # Create dict for preprocessing
        data_frames = {
            'Games': games_df.copy(),
            'Points': points_df.copy(),
            'Players': players_df.copy()
        }
        
        # Preprocess and validate
        self._preprocess_data(data_frames)
        
        # Process games and calculate points
        games_df = self._process_games(data_frames['Games'], data_frames['Points'])
        points_df = self._calculate_points(
            data_frames['Points'],
            games_df,
            data_frames['Players']
        )
        
        logger.info(f"Processing complete: {len(games_df)} games, {len(points_df)} point records")
        return games_df, points_df
    
    def _load_data(self, input_path: Path) -> Dict[str, pd.DataFrame]:
        """Load all required sheets from Excel file."""
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        sheet_names = ['Games', 'Parameters', 'Points', 'Players']
        logger.info(f"Loading sheets: {sheet_names}")
        return pd.read_excel(input_path, sheet_name=sheet_names)
    
    def _load_config(self, parameters_df: pd.DataFrame) -> None:
        """Load scoring configuration from Parameters sheet."""
        logger.info("Loading scoring configuration")
        parameters_df = parameters_df.set_index('Parameter')
        
        match_parameters = {}
        for match_type in ['5-a-side', '7-a-side', '11-a-side']:
            if match_type in parameters_df.columns:
                match_parameters[match_type] = parameters_df[match_type].to_dict()
            else:
                logger.warning(f"Missing configuration for {match_type}")
        
        self.config = {'match_parameters': match_parameters}
    
    def _preprocess_data(self, data_frames: Dict[str, pd.DataFrame]) -> None:
        """Preprocess and validate data."""
        # Standardize player names
        for df_name in ['Points', 'Players']:
            if 'Player' in data_frames[df_name].columns:
                data_frames[df_name]['Player'] = data_frames[df_name]['Player'].str.strip()
        
        # Convert dates
        for df_name in ['Games', 'Points']:
            if 'Date' in data_frames[df_name].columns:
                data_frames[df_name]['Date'] = pd.to_datetime(
                    data_frames[df_name]['Date'], 
                    errors='coerce'
                )
    
    def _process_games(self, games_df: pd.DataFrame, points_df: pd.DataFrame) -> pd.DataFrame:
        """Process games data with season, gameweek, and match type."""
        df = games_df.copy()
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Winning team
        df['Winning Team'] = df.apply(
            lambda row: 'Team A' if row['Team A Goals'] > row['Team B Goals']
            else 'Team B' if row['Team B Goals'] > row['Team A Goals']
            else 'Draw',
            axis=1
        )
        
        # Calculate seasons
        df['Season'] = df['Date'].apply(
            lambda d: calculate_season_from_date(d.date()) if pd.notna(d) else None
        )
        
        # Apply championship split logic
        df = self._apply_championship_split(df, points_df)
        
        # Per-championship season renumbering (each championship starts from Season 1)
        for champ in df['Championship'].unique():
            mask = df['Championship'] == champ
            champ_seasons = sorted(df.loc[mask, 'Season'].dropna().unique())
            if champ_seasons:
                season_map = {old: new + 1 for new, old in enumerate(champ_seasons)}
                df.loc[mask, 'Season'] = df.loc[mask, 'Season'].map(season_map)
        
        # Log per-championship season ranges
        season_ranges = df.groupby('Championship')['Season'].agg(['min', 'max'])
        logger.info(f"Per-championship seasons: {season_ranges.to_dict('index')}")
        
        # Calculate gameweeks per championship per season
        df['Gameweek'] = df.groupby(['Season', 'Championship']).cumcount() + 1
        
        # Determine match type from number of players
        player_counts = points_df.groupby('Date').size()
        df['Number of Players'] = df['Date'].map(player_counts)
        df['Match Type'] = df['Number of Players'].apply(
            lambda x: MatchType.from_players(x).value if pd.notna(x) else None
        )
        
        return df[[
            'Date', 'Season', 'Gameweek', 'Match Type', 'Championship',
            'Winning Team', 'Team A Goals', 'Team B Goals', 'Number of Players'
        ]]
    
    def _apply_championship_split(
        self, 
        games_df: pd.DataFrame, 
        points_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Apply championship split logic.
        
        If "Championship" column exists in games_df, use it.
        Otherwise, apply retroactive rule:
        - 5-a-side games (≤10 players) from 2024+ → Lambrate
        - Everything else → Bovisa
        """
        if 'Championship' in games_df.columns:
            logger.info("Using existing Championship column")
            return games_df
        
        logger.info("Applying retroactive championship split")
        
        # Count players per game
        player_counts = points_df.groupby('Date').size()
        games_df['Number of Players'] = games_df['Date'].map(player_counts)
        
        # Apply rule
        def assign_championship(row: pd.Series) -> str:
            if pd.isna(row['Date']) or pd.isna(row['Number of Players']):
                return CHAMPIONSHIP_CONFIG.default_championship
            
            year = row['Date'].year
            num_players = row['Number of Players']
            
            # 5-a-side from 2024+ → Lambrate
            if (year >= CHAMPIONSHIP_CONFIG.lambrate_cutoff_year and 
                num_players <= CHAMPIONSHIP_CONFIG.lambrate_max_players):
                return CHAMPIONSHIP_CONFIG.lambrate_championship
            
            return CHAMPIONSHIP_CONFIG.default_championship
        
        games_df['Championship'] = games_df.apply(assign_championship, axis=1)
        logger.info(f"Championship split: {games_df['Championship'].value_counts().to_dict()}")
        
        return games_df
    
    def _calculate_points(
        self,
        points_df: pd.DataFrame,
        games_df: pd.DataFrame,
        players_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Calculate all point components for each player."""
        # Merge with games data
        # If both DataFrames have Championship column, merge on both Date and Championship
        merge_on = ['Date']
        if 'Championship' in points_df.columns and 'Championship' in games_df.columns:
            merge_on.append('Championship')
        
        df = pd.merge(points_df, games_df, on=merge_on, how='left')
        
        # Drop rows where merge failed (no matching game)
        missing_games = df['Match Type'].isna().sum()
        if missing_games > 0:
            logger.warning(f"Dropping {missing_games} point records with no matching game")
            df = df[df['Match Type'].notna()]
        
        # Fill missing numeric values
        numeric_cols = ['Goals', 'Own Goals', 'SPL Bonus', 'MVP', 'Friend Referrals', 'Penalty']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Assign positions
        df = self._assign_positions(df, players_df)
        
        # Calculate goal difference
        df['Goal Difference'] = df.apply(self._calculate_goal_difference, axis=1)
        df['Game Outcome'] = df['Goal Difference'].apply(
            lambda x: GameOutcome.from_goal_diff(x).value
        )
        
        # Calculate all point components
        df = self._calculate_all_points(df)
        
        return df
    
    def _assign_positions(
        self, 
        df: pd.DataFrame, 
        players_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Assign player positions based on game data or defaults."""
        column_map = {
            "5-a-side": "Default 5 Position",
            "7-a-side": "Default 7 Position",
            "11-a-side": "Default 11 Position"
        }
        
        def get_position(row: pd.Series) -> str:
            # Use game-specific position if available
            if pd.notna(row.get('Game Position')) and row.get('Game Position') != '':
                return row['Game Position']
            
            # Fallback to default position
            col_name = column_map.get(row['Match Type'])
            if col_name and col_name in row:
                default_pos = row.get(col_name)
                if pd.notna(default_pos) and default_pos != '':
                    return default_pos
            
            return 'Unknown'
        
        df['Position'] = df.apply(get_position, axis=1)
        return df
    
    def _calculate_goal_difference(self, row: pd.Series) -> int:
        """Calculate goal difference for a player's team."""
        team_a_goals = row['Team A Goals'] if pd.notna(row['Team A Goals']) else 0
        team_b_goals = row['Team B Goals'] if pd.notna(row['Team B Goals']) else 0
        
        if row['Team'] == 'Team A':
            return int(team_a_goals - team_b_goals)
        return int(team_b_goals - team_a_goals)
    
    def _calculate_all_points(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all point components and total."""
        # Base points
        df['Participation Points'] = df.apply(
            lambda row: self.config['match_parameters'][row['Match Type']]['Participation'],
            axis=1
        )
        
        # Performance points
        point_categories = {
            'Goals': 'Goal',
            'Own Goals': 'Own Goal',
            'SPL Bonus': 'SPL Bonus',
            'MVP': 'MVP',
            'Friend Referrals': 'Friend Referrals',
            'Penalty': 'Penalty'
        }
        
        for col, param in point_categories.items():
            df[f'{param} Points'] = df.apply(
                lambda row: row[col] * self.config['match_parameters'][row['Match Type']][param],
                axis=1
            )
        
        # Positional points
        df['Goals Conceded'] = df.apply(
            lambda row: row['Team B Goals'] if row['Team'] == 'Team A' else row['Team A Goals'],
            axis=1
        )
        
        df['Goalkeeper Points'] = df.apply(
            lambda row: self.config['match_parameters'][row['Match Type']]['Goalkeeper Score']
            if row['Position'] == 'Goalkeeper' else 0,
            axis=1
        )
        
        df['Defensive Score Points'] = df.apply(self._calculate_defensive_score, axis=1)
        df['Midfield Score'] = df.apply(self._calculate_midfield_score, axis=1)
        
        # Outcome points
        df['Game Outcome Points'] = df.apply(
            lambda row: self.config['match_parameters'][row['Match Type']][row['Game Outcome']],
            axis=1
        )
        
        # Total
        point_columns = [
            'Participation Points', 'Goal Points', 'Own Goal Points',
            'SPL Bonus Points', 'MVP Points', 'Friend Referrals Points',
            'Goalkeeper Points', 'Defensive Score Points', 'Midfield Score',
            'Penalty Points', 'Game Outcome Points'
        ]
        df['Total Points'] = df[point_columns].sum(axis=1)
        
        return df
    
    def _calculate_defensive_score(self, row: pd.Series) -> float:
        """Calculate defensive score based on position."""
        base_score = (
            self.config['match_parameters'][row['Match Type']]['Defensive Score'] -
            row['Goals Conceded']
        )
        
        if row['Position'] in ['Goalkeeper', 'Defender', 'Defensive']:
            return max(base_score, 0)
        elif row['Position'] in ['Midfielder', 'Outfield']:
            return max(math.ceil(base_score / 2), 0)
        elif row['Position'] in ['Forward', 'Offensive']:
            return 0
        return 0
    
    def _calculate_midfield_score(self, row: pd.Series) -> float:
        """Calculate midfield score based on position."""
        if row['Position'] in ['Midfielder', 'Offensive', 'Outfield']:
            return max(row['Goal Difference'], 0)
        elif row['Position'] == 'Forward':
            return max(math.ceil(row['Goal Difference'] / 2), 0)
        return 0
