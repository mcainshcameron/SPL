"""
Fantasy League Processor
Processes fantasy team data and generates standings.
Ported from Fanta_Team_gen and Fanta_Table scripts.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class FantasyProcessor:
    """Processes fantasy league data."""
    
    def process_fantasy_league(
        self,
        fantasy_file: Path,
        points_df: pd.DataFrame,
        season: Optional[int] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Process fantasy league data.
        
        Args:
            fantasy_file: Path to fantasy squads Excel file
            points_df: Processed points data
            season: Season to process (None = all seasons)
            
        Returns:
            Dict with 'standings' and 'teams' DataFrames
        """
        logger.info(f"Processing fantasy league from {fantasy_file}")
        
        if not fantasy_file.exists():
            logger.warning(f"Fantasy file not found: {fantasy_file}")
            return {'standings': pd.DataFrame(), 'teams': pd.DataFrame()}
        
        # Load fantasy data
        fantasy_data = pd.read_excel(fantasy_file)
        
        # Filter points by season if specified
        if season is not None:
            season_points = points_df[points_df['Season'] == season]
        else:
            season_points = points_df
        
        # Process team selections
        team_data = self._process_team_selections(fantasy_data, season_points)
        
        # Generate standings
        standings = self._generate_standings(team_data)
        
        # Generate team rosters
        teams = self._generate_team_rosters(team_data)
        
        logger.info(f"Processed {len(standings)} fantasy teams")
        
        return {
            'standings': standings,
            'teams': teams
        }
    
    def _process_team_selections(
        self,
        fantasy_data: pd.DataFrame,
        points_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Process player selections and merge with points."""
        # Get player selection columns (skip owner and team name columns)
        selection_cols = [
            col for col in fantasy_data.columns
            if col not in ['Nome e Cognome', 'Nome della tua squadra FantaSPL']
        ]
        
        # Melt to long format
        player_selection = fantasy_data.melt(
            id_vars=['Nome e Cognome', 'Nome della tua squadra FantaSPL'],
            value_vars=selection_cols,
            value_name='Selection'
        ).drop(columns='variable')
        
        # Split comma-separated values and explode
        player_selection['Selection'] = player_selection['Selection'].astype(str)
        player_selection['Selection'] = player_selection['Selection'].apply(
            lambda x: x.split(', ') if ', ' in x else [x]
        )
        player_selection = player_selection.explode('Selection').reset_index(drop=True)
        
        # Clean up
        player_selection['Selection'] = player_selection['Selection'].replace('nan', np.nan)
        player_selection = player_selection.dropna(subset=['Selection'])
        player_selection['Selection'] = player_selection['Selection'].str.strip()
        
        # Merge with points data
        merged = player_selection.merge(
            points_df[['Player', 'Total Points']],
            left_on='Selection',
            right_on='Player',
            how='left'
        )
        
        # Fill missing points with 0
        merged['Total Points'] = merged['Total Points'].fillna(0)
        
        return merged
    
    def _generate_standings(self, team_data: pd.DataFrame) -> pd.DataFrame:
        """Generate fantasy league standings."""
        standings = (
            team_data
            .groupby(['Nome e Cognome', 'Nome della tua squadra FantaSPL'])
            .agg({'Total Points': 'sum'})
            .reset_index()
            .sort_values('Total Points', ascending=False)
            .reset_index(drop=True)
        )
        
        # Rename columns
        standings.rename(columns={
            'Nome e Cognome': 'Owner',
            'Nome della tua squadra FantaSPL': 'Team Name',
            'Total Points': 'Total Points'
        }, inplace=True)
        
        # Add rank
        standings['Rank'] = standings['Total Points'].rank(
            method='min',
            ascending=False
        ).astype(int)
        
        # Add rank change (will be calculated later with historical data)
        standings['Rank Change'] = 0
        
        # Reorder columns
        standings = standings[['Rank', 'Team Name', 'Owner', 'Total Points', 'Rank Change']]
        
        return standings
    
    def _generate_team_rosters(self, team_data: pd.DataFrame) -> pd.DataFrame:
        """Generate detailed team rosters."""
        rosters = (
            team_data
            .groupby(['Nome e Cognome', 'Nome della tua squadra FantaSPL', 'Selection'])
            .agg({'Total Points': 'sum'})
            .reset_index()
        )
        
        rosters.rename(columns={
            'Nome e Cognome': 'Owner',
            'Nome della tua squadra FantaSPL': 'Team Name',
            'Selection': 'Player',
            'Total Points': 'Player Points'
        }, inplace=True)
        
        # Sort by team and points
        rosters = rosters.sort_values(
            ['Team Name', 'Player Points'],
            ascending=[True, False]
        ).reset_index(drop=True)
        
        return rosters
    
    def calculate_rank_changes(
        self,
        current_standings: pd.DataFrame,
        previous_standings: Optional[pd.DataFrame]
    ) -> pd.DataFrame:
        """
        Calculate rank changes between two standings.
        
        Args:
            current_standings: Current fantasy standings
            previous_standings: Previous standings (or None)
            
        Returns:
            Updated current_standings with Rank Change
        """
        if previous_standings is None or len(previous_standings) == 0:
            current_standings['Rank Change'] = 0
            return current_standings
        
        # Create mapping of team to previous rank
        prev_ranks = dict(zip(
            previous_standings['Team Name'],
            previous_standings['Rank']
        ))
        
        # Calculate changes
        def calc_change(row: pd.Series) -> int:
            team = row['Team Name']
            current_rank = row['Rank']
            prev_rank = prev_ranks.get(team, current_rank)
            # Positive = moved up
            return int(prev_rank - current_rank)
        
        current_standings['Rank Change'] = current_standings.apply(calc_change, axis=1)
        
        return current_standings
