"""
SPLNews Generator
Auto-generates Italian headlines from market value changes.
"""

import logging
from datetime import datetime
from typing import Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


class NewsGenerator:
    """Generates SPLNews headlines from market data."""
    
    def generate_news(
        self,
        weekly_values: pd.DataFrame,
        player_summaries: Dict[str, pd.DataFrame]
    ) -> List[Dict[str, str]]:
        """
        Generate news headlines from market changes.
        
        Args:
            weekly_values: Weekly market values with changes
            player_summaries: Player summaries by championship
            
        Returns:
            List of news items with headline and type
        """
        logger.info("Generating SPLNews headlines")
        
        news_items = []
        
        # Get latest week data
        if 'Week' in weekly_values.columns:
            latest_week = weekly_values['Week'].max()
            latest_data = weekly_values[weekly_values['Week'] == latest_week]
        else:
            latest_data = weekly_values
        
        # Generate different types of headlines
        news_items.extend(self._generate_gainer_headlines(latest_data))
        news_items.extend(self._generate_loser_headlines(latest_data))
        news_items.extend(self._generate_milestone_headlines(latest_data))
        news_items.extend(self._generate_debut_headlines(latest_data))
        news_items.extend(self._generate_streak_headlines(latest_data))
        
        # Add timestamp
        for item in news_items:
            item['timestamp'] = datetime.now().isoformat()
        
        logger.info(f"Generated {len(news_items)} news headlines")
        
        return news_items
    
    def _generate_gainer_headlines(self, latest_data: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate headlines for biggest gainers."""
        headlines = []
        
        if 'Value Change' not in latest_data.columns:
            return headlines
        
        # Get top 3 gainers
        gainers = latest_data.nlargest(3, 'Value Change')
        
        for _, row in gainers.iterrows():
            if row['Value Change'] <= 0:
                continue
            
            player = row['Player']
            change = row['Value Change']
            change_pct = row.get('Value Change %', 0)
            
            # Format change
            change_str = self._format_value(change)
            
            # Generate variations of headlines
            headlines_variants = [
                f"{player} in forte rialzo: +{change_str} questa settimana",
                f"Boom per {player}: valore su di {change_str} (+{change_pct:.1f}%)",
                f"{player} schizza in alto: +{change_str} sul mercato",
                f"Grande prestazione per {player}: mercato premia con +{change_str}"
            ]
            
            # Pick first variant
            headlines.append({
                'type': 'gainer',
                'headline': headlines_variants[0],
                'player': player
            })
        
        return headlines
    
    def _generate_loser_headlines(self, latest_data: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate headlines for biggest losers."""
        headlines = []
        
        if 'Value Change' not in latest_data.columns:
            return headlines
        
        # Get top 3 losers (most negative change)
        losers = latest_data.nsmallest(3, 'Value Change')
        
        for _, row in losers.iterrows():
            if row['Value Change'] >= 0:
                continue
            
            player = row['Player']
            change = abs(row['Value Change'])
            change_pct = abs(row.get('Value Change %', 0))
            weeks_absent = row.get('Weeks Since Last Game', 0)
            
            # Format change
            change_str = self._format_value(change)
            
            # Different messages based on reason
            if weeks_absent > 1:
                headline = f"{player} crolla del {change_pct:.0f}%: {int(weeks_absent)} settimane di assenza"
            else:
                headline = f"{player} in difficoltà: perde {change_str} di valore (-{change_pct:.1f}%)"
            
            headlines.append({
                'type': 'loser',
                'headline': headline,
                'player': player
            })
        
        return headlines
    
    def _generate_milestone_headlines(self, latest_data: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate headlines for milestone achievements."""
        headlines = []
        
        # Check for players reaching milestone values
        milestones = [
            (20_000_000, "20M"),
            (15_000_000, "15M"),
            (10_000_000, "10M"),
            (5_000_000, "5M")
        ]
        
        for threshold, label in milestones:
            milestone_players = latest_data[
                (latest_data['Market Value'] >= threshold) &
                (latest_data['Market Value'] - latest_data.get('Value Change', 0) < threshold)
            ]
            
            for _, row in milestone_players.head(2).iterrows():
                player = row['Player']
                value = self._format_value(row['Market Value'])
                
                headlines.append({
                    'type': 'milestone',
                    'headline': f"{player} supera i €{label}: nuovo traguardo raggiunto!",
                    'player': player
                })
        
        return headlines
    
    def _generate_debut_headlines(self, latest_data: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate headlines for player debuts."""
        headlines = []
        
        # Find players with only 1 game
        if 'Games Played' in latest_data.columns:
            debuts = latest_data[latest_data['Games Played'] == 1]
            
            for _, row in debuts.head(3).iterrows():
                player = row['Player']
                value = self._format_value(row['Market Value'])
                
                headlines.append({
                    'type': 'debut',
                    'headline': f"Benvenuto {player}! Debutto con valore iniziale di {value}",
                    'player': player
                })
        
        return headlines
    
    def _generate_streak_headlines(self, latest_data: pd.DataFrame) -> List[Dict[str, str]]:
        """Generate headlines for win/attendance streaks."""
        headlines = []
        
        # Find players with long attendance streaks
        if 'Week Streak' in latest_data.columns:
            streak_players = latest_data[latest_data['Week Streak'] >= 5].nlargest(
                3, 'Week Streak'
            )
            
            for _, row in streak_players.iterrows():
                player = row['Player']
                streak = int(row['Week Streak'])
                
                headlines.append({
                    'type': 'streak',
                    'headline': f"{player} inarrestabile: {streak} settimane consecutive sul campo",
                    'player': player
                })
        
        return headlines
    
    def _format_value(self, value: float) -> str:
        """Format value in millions with proper Italian notation."""
        millions = value / 1_000_000
        
        if millions >= 1:
            return f"€{millions:.1f}M"
        else:
            thousands = value / 1000
            return f"€{thousands:.0f}K"
