"""
Market Value Calculator
EWMA-based market valuation model.
Ported from market_values_v_03.ipynb with improvements.
"""

import logging
from typing import Dict, List

import numpy as np
import pandas as pd

from .config import MARKET_CONFIG

logger = logging.getLogger(__name__)


class MarketCalculator:
    """Calculates player market values using EWMA model."""
    
    def __init__(self) -> None:
        self.config = MARKET_CONFIG
    
    def calculate_weekly_values(self, points_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate market values week by week.
        
        Args:
            points_df: Processed points data with all necessary columns
            
        Returns:
            DataFrame with weekly market values per player
        """
        logger.info("Calculating weekly market values")
        
        # Prepare data
        df = self._prepare_data(points_df)
        
        # Get all weeks and players
        all_weeks = sorted(df['Week'].unique())
        logger.info(f"Processing {len(all_weeks)} weeks")
        
        weekly_values = []
        
        for week in all_weeks:
            week_values = self._calculate_week_values(df, week, all_weeks)
            weekly_values.append(week_values)
        
        result = pd.concat(weekly_values, ignore_index=True)
        logger.info(f"Calculated values for {len(result)} player-week combinations")
        
        return result
    
    def _prepare_data(self, points_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for market value calculation."""
        df = points_df.copy()
        
        # Ensure Date is datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Create week identifier
        df['Week'] = df['Date'].dt.to_period('W')
        
        # Map game outcome to numeric
        outcome_mapping = {'Loss': -1, 'Draw': 0, 'Win': 1}
        df['Game Outcome Numeric'] = df['Game Outcome'].map(outcome_mapping)
        
        return df
    
    def _calculate_week_values(
        self,
        df: pd.DataFrame,
        current_week: pd.Period,
        all_weeks: List[pd.Period]
    ) -> pd.DataFrame:
        """Calculate market values for a specific week."""
        # Filter data up to current week
        df_filtered = df[df['Week'] <= current_week].copy()
        
        # Aggregate by week and player
        numeric_columns = [
            'Goals', 'Own Goals', 'SPL Bonus', 'MVP', 'Friend Referrals',
            'Penalty', 'Goal Difference', 'Goals Conceded', 'Game Outcome Numeric',
            'Defensive Score Points', 'Midfield Score', 'Total Points'
        ]
        
        df_agg = df_filtered.groupby(['Week', 'Player'])[numeric_columns].mean().reset_index()
        df_agg = df_agg.sort_values(['Week', 'Player'])
        
        # Calculate EWMA for each player
        player_stats = df_agg.groupby('Player').apply(
            lambda x: x.set_index('Week')[numeric_columns].ewm(
                span=self.config.ewma_span
            ).mean().iloc[-1]
        ).reset_index()
        
        # Calculate additional stats
        player_stats['Games Played'] = df_agg.groupby('Player')['Week'].count().values
        player_stats['Sum Total Points'] = df_agg.groupby('Player')['Total Points'].sum().values
        
        # Calculate recency (weeks since last game)
        player_stats['Last Game Week'] = df_agg.groupby('Player')['Week'].max().values
        player_stats['Weeks Since Last Game'] = (
            (current_week.to_timestamp() - player_stats['Last Game Week'].dt.to_timestamp()).dt.days / 7
        ).astype(int)
        
        # Recency decay factor
        player_stats['Recency Factor'] = np.exp(
            -self.config.decay_rate * player_stats['Weeks Since Last Game']
        )
        
        # Calculate week streak
        week_list = all_weeks[:all_weeks.index(current_week) + 1]
        player_stats['Week Streak'] = df_filtered.groupby('Player').apply(
            lambda x: self._calculate_week_streak(x, week_list)
        ).values
        
        # Reset streak if player hasn't played recently
        player_stats.loc[player_stats['Weeks Since Last Game'] > 0, 'Week Streak'] = 0
        
        # Streak bonus
        player_stats['Streak Bonus Factor'] = 1 + (
            self.config.streak_bonus_rate * player_stats['Week Streak']
        )
        
        # Adjusted total points (with recency and streak)
        player_stats['Adjusted Total Points'] = (
            player_stats['Total Points'] *
            player_stats['Recency Factor'] *
            player_stats['Streak Bonus Factor']
        ).round(2)
        
        # Calculate KPI
        player_stats['KPI'] = player_stats.apply(
            lambda row: self._calculate_kpi(row), axis=1
        )
        
        # Normalize KPI to 0-100
        min_kpi = player_stats['KPI'].min()
        max_kpi = player_stats['KPI'].max()
        if max_kpi > min_kpi:
            player_stats['KPI'] = (
                100 * (player_stats['KPI'] - min_kpi) / (max_kpi - min_kpi)
            ).round(2)
        else:
            player_stats['KPI'] = 50.0
        
        # Calculate games played percentage
        min_games = player_stats['Games Played'].min()
        max_games = player_stats['Games Played'].max()
        if max_games > min_games:
            player_stats['Games Played %'] = (
                (player_stats['Games Played'] - min_games) / (max_games - min_games) * 100
            ).round(2)
        else:
            player_stats['Games Played %'] = 100.0
        
        # Calculate market value
        player_stats['Market Value'] = player_stats.apply(
            lambda row: self._calculate_market_value(row, player_stats), axis=1
        )
        
        # Add week identifier
        player_stats['Week'] = current_week
        
        # Select final columns
        final_cols = [
            'Player', 'Week', 'Games Played', 'Week Streak',
            'Adjusted Total Points', 'Sum Total Points', 'KPI',
            'Weeks Since Last Game', 'Market Value'
        ]
        
        return player_stats[final_cols].sort_values(
            'Market Value', ascending=False
        ).reset_index(drop=True)
    
    def _calculate_week_streak(self, group: pd.DataFrame, all_game_weeks: List[pd.Period]) -> int:
        """Calculate current consecutive week streak for a player."""
        player_weeks = set(group['Week'])
        
        if not player_weeks:
            return 0
        
        streak = 0
        for week in reversed(all_game_weeks):
            if week in player_weeks:
                streak += 1
            elif streak > 0:
                break
        
        return streak
    
    def _calculate_kpi(self, row: pd.Series) -> float:
        """Calculate KPI from weighted metrics."""
        kpi = 0.0
        weights = self.config.kpi_weights
        
        for metric, weight in weights.items():
            if metric == 'Game Outcome':
                # Use numeric outcome
                value = row.get('Game Outcome Numeric', 0)
            else:
                value = row.get(metric, 0)
            
            kpi += value * weight
        
        return kpi
    
    def _calculate_market_value(self, row: pd.Series, all_stats: pd.DataFrame) -> int:
        """
        Calculate market value from normalized components.
        Uses exponential scaling to spread values across the range.
        """
        # Normalize each component
        norm_values = {}
        for metric in self.config.market_weights.keys():
            min_val = all_stats[metric].min()
            max_val = all_stats[metric].max()
            
            if max_val > min_val:
                norm_values[metric] = (row[metric] - min_val) / (max_val - min_val)
            else:
                norm_values[metric] = 0.5
        
        # Calculate weighted score
        weighted_score = sum(
            norm_values[metric] * weight
            for metric, weight in self.config.market_weights.items()
        )
        
        # Apply exponential scaling for better distribution
        exp_score = np.exp(weighted_score) - 1
        max_exp = np.exp(1) - 1
        
        market_value = (
            self.config.min_value +
            (self.config.max_value - self.config.min_value) * (exp_score / max_exp)
        )
        
        # Round to nearest 100k
        return int(round(market_value, -5))
    
    def get_latest_values(self, weekly_values: pd.DataFrame) -> pd.DataFrame:
        """
        Get the most recent market value for each player.
        
        Args:
            weekly_values: Full weekly values DataFrame
            
        Returns:
            DataFrame with latest value per player
        """
        return (
            weekly_values
            .sort_values('Week')
            .groupby('Player')
            .last()
            .reset_index()
            .sort_values('Market Value', ascending=False)
        )
    
    def calculate_value_changes(self, weekly_values: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate week-over-week value changes.
        
        Args:
            weekly_values: Full weekly values DataFrame
            
        Returns:
            DataFrame with value change columns added
        """
        df = weekly_values.copy().sort_values(['Player', 'Week'])
        
        # Calculate previous value
        df['Previous Value'] = df.groupby('Player')['Market Value'].shift(1)
        
        # Calculate change
        df['Value Change'] = df['Market Value'] - df['Previous Value'].fillna(df['Market Value'])
        df['Value Change %'] = (
            (df['Value Change'] / df['Previous Value']) * 100
        ).round(1)
        
        return df
