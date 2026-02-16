"""
Player Summary Generator
Generates player summaries and rankings.
Ported from Points_Summary_v.0.6.py with improvements.
"""

import logging
from typing import Dict, List, Optional

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class PlayerSummarizer:
    """Generates player summaries and rankings."""
    
    def generate_summaries(
        self,
        points_df: pd.DataFrame,
        games_df: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """
        Generate player summaries for each championship + combined.
        
        Args:
            points_df: Processed points data
            games_df: Processed games data
            
        Returns:
            Dict mapping championship name to summary DataFrame
        """
        logger.info("Generating player summaries")
        
        summaries = {}
        
        # Get all championships
        championships = points_df['Championship'].unique() if 'Championship' in points_df.columns else ['All']
        
        # Generate summary for each championship
        for championship in championships:
            if championship == 'All':
                champ_data = points_df
            else:
                champ_data = points_df[points_df['Championship'] == championship]
            
            summary = self._compute_summary(champ_data, games_df)
            summaries[championship] = summary
            logger.info(f"Generated summary for {championship}: {len(summary)} players")
        
        # Also generate combined summary across all championships
        if len(championships) > 1:
            combined = self._compute_summary(points_df, games_df)
            summaries['Combined'] = combined
            logger.info(f"Generated combined summary: {len(combined)} players")
        
        return summaries
    
    def _compute_summary(
        self,
        points_df: pd.DataFrame,
        games_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Compute summary statistics for players."""
        # Define aggregations
        aggs = {
            'Games Played': ('Date', 'count'),
            'Penalties': ('Penalty', 'sum'),
            'Friend Referrals': ('Friend Referrals', 'sum'),
            'Own Goals': ('Own Goals', 'sum'),
            'Goals Conceded': ('Goals Conceded', 'sum'),
            'Average Goals': ('Goals', 'mean'),
            'Total Goals': ('Goals', 'sum'),
            'PPG': ('Total Points', 'mean'),
            'Total Points': ('Total Points', 'sum'),
            'MVP': ('MVP', 'sum'),
            'SPL Bonus': ('SPL Bonus', 'sum')
        }
        
        summary = points_df.groupby('Player').agg(**aggs).reset_index()
        
        # Calculate wins
        wins = points_df[points_df['Game Outcome'] == 'Win'].groupby('Player').size()
        summary['Wins'] = summary['Player'].map(wins).fillna(0).astype(int)
        
        # Calculate win percentage
        summary['Win %'] = (summary['Wins'] / summary['Games Played'] * 100).round(1)
        
        # Calculate rank
        summary['Rank'] = summary['Total Points'].rank(
            method='min', 
            ascending=False
        ).astype(int)
        
        # Calculate rank change (will be updated with historical data)
        summary['Rank Change'] = 0
        
        # Round floats
        summary['Average Goals'] = summary['Average Goals'].round(2)
        summary['PPG'] = summary['PPG'].round(2)
        
        # Convert to int where appropriate
        int_cols = [
            'Games Played', 'Wins', 'Penalties', 'Friend Referrals',
            'Own Goals', 'Goals Conceded', 'Total Goals', 'MVP', 'SPL Bonus'
        ]
        for col in int_cols:
            if col in summary.columns:
                summary[col] = summary[col].fillna(0).astype(int)
        
        # Reorder columns
        columns = [
            'Player', 'Rank', 'Games Played', 'Wins', 'Win %',
            'Total Goals', 'Average Goals', 'PPG', 'Total Points',
            'MVP', 'SPL Bonus', 'Penalties', 'Friend Referrals',
            'Own Goals', 'Goals Conceded', 'Rank Change'
        ]
        
        summary = summary[columns].sort_values('Rank').reset_index(drop=True)
        
        return summary
    
    def generate_season_summaries(
        self,
        points_df: pd.DataFrame,
        games_df: pd.DataFrame
    ) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Generate summaries broken down by season and championship.
        
        Returns:
            Nested dict: {season: {championship: summary_df}}
        """
        logger.info("Generating season summaries")
        
        season_summaries = {}
        
        # Get all unique seasons
        seasons = sorted(points_df['Season'].dropna().unique())
        
        for season in seasons:
            season_data = points_df[points_df['Season'] == season]
            season_games = games_df[games_df['Season'] == season]
            
            # Generate summaries for this season
            summaries = self.generate_summaries(season_data, season_games)
            season_summaries[f"Season {int(season)}"] = summaries
            
            logger.info(f"Generated summaries for Season {int(season)}")
        
        # Also generate total (all seasons)
        total_summaries = self.generate_summaries(points_df, games_df)
        season_summaries['Total'] = total_summaries
        
        return season_summaries
    
    def calculate_rank_changes(
        self,
        current_summary: pd.DataFrame,
        previous_summary: Optional[pd.DataFrame]
    ) -> pd.DataFrame:
        """
        Calculate rank changes between two summaries.
        
        Args:
            current_summary: Current ranking
            previous_summary: Previous ranking (or None)
            
        Returns:
            Updated current_summary with Rank Change column
        """
        if previous_summary is None:
            current_summary['Rank Change'] = 0
            return current_summary
        
        # Create mapping of player to previous rank
        prev_ranks = dict(zip(previous_summary['Player'], previous_summary['Rank']))
        
        # Calculate changes
        def calc_change(row: pd.Series) -> int:
            player = row['Player']
            current_rank = row['Rank']
            prev_rank = prev_ranks.get(player, current_rank)
            # Positive = moved up (lower rank number)
            return int(prev_rank - current_rank)
        
        current_summary['Rank Change'] = current_summary.apply(calc_change, axis=1)
        
        return current_summary
