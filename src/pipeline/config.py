"""
SPL Pipeline Configuration
All configurable parameters for scoring, market valuations, and processing.
"""

from dataclasses import dataclass
from typing import Dict
from datetime import date


@dataclass
class SeasonConfig:
    """Season configuration."""
    start_month: int = 9  # September
    start_day: int = 1
    end_month: int = 7  # July
    end_day: int = 30


@dataclass
class MarketConfig:
    """Market valuation configuration."""
    ewma_span: int = 8
    decay_rate: float = 0.05
    streak_bonus_rate: float = 0.04
    min_value: int = 1_000_000  # €1M
    max_value: int = 25_000_000  # €25M
    
    # KPI weights for market value calculation
    kpi_weights: Dict[str, float] = None
    
    # Market value component weights
    market_weights: Dict[str, float] = None
    
    def __post_init__(self) -> None:
        if self.kpi_weights is None:
            self.kpi_weights = {
                'Goals': 1.0,
                'Own Goals': -1.0,
                'SPL Bonus': 1.0,
                'MVP': 3.0,
                'Friend Referrals': 3.0,
                'Penalty': -5.0,
                'Goal Difference': 0.5,
                'Game Outcome': 3.0,
                'Goals Conceded': -0.5,
                'Defensive Score Points': 0.5,
                'Midfield Score': 0.5
            }
        
        if self.market_weights is None:
            self.market_weights = {
                'Games Played %': 0.6,
                'Adjusted Total Points': 0.15,
                'KPI': 0.25
            }


@dataclass
class ChampionshipConfig:
    """Championship split configuration."""
    # If no Championship column exists in Excel, apply retroactive rule:
    # 5-a-side games (≤10 players) from 2024+ → "Lambrate"
    # Everything else → "Bovisa"
    default_championship: str = "Bovisa"
    lambrate_championship: str = "Lambrate"
    lambrate_cutoff_year: int = 2024
    lambrate_max_players: int = 10


@dataclass
class ScoringParameters:
    """Scoring parameters for different game formats."""
    # Parameters from Excel Parameters sheet (verified from FantaSPL_Milano.xlsx)
    parameters: Dict[str, Dict[str, int]] = None
    
    def __post_init__(self) -> None:
        if self.parameters is None:
            self.parameters = {
                '5-a-side': {
                    'Win': 3,
                    'Draw': 1,
                    'Loss': 0,
                    'Participation': 4,
                    'Goal': 1,
                    'Own Goal': -2,
                    'Penalty': -3,
                    'SPL Bonus': 3,
                    'MVP': 3,
                    'Friend Referrals': 3,
                    'Defensive Score': 10,
                    'Goalkeeper Score': 1
                },
                '7-a-side': {
                    'Win': 3,
                    'Draw': 1,
                    'Loss': 0,
                    'Participation': 5,
                    'Goal': 1,
                    'Own Goal': -2,
                    'Penalty': -4,
                    'SPL Bonus': 3,
                    'MVP': 3,
                    'Friend Referrals': 4,
                    'Defensive Score': 10,
                    'Goalkeeper Score': 1
                },
                '11-a-side': {
                    'Win': 3,
                    'Draw': 1,
                    'Loss': 0,
                    'Participation': 6,
                    'Goal': 2,
                    'Own Goal': -2,
                    'Penalty': -5,
                    'SPL Bonus': 5,
                    'MVP': 5,
                    'Friend Referrals': 5,
                    'Defensive Score': 8,
                    'Goalkeeper Score': 1
                }
            }


# Global configuration instances
SEASON_CONFIG = SeasonConfig()
MARKET_CONFIG = MarketConfig()
CHAMPIONSHIP_CONFIG = ChampionshipConfig()
SCORING_PARAMETERS = ScoringParameters()


def get_season_boundaries(year: int) -> tuple[date, date]:
    """
    Get season start and end dates for a given year.
    
    Args:
        year: The year of the season start
        
    Returns:
        Tuple of (season_start, season_end) dates
    """
    season_start = date(year, SEASON_CONFIG.start_month, SEASON_CONFIG.start_day)
    season_end = date(year + 1, SEASON_CONFIG.end_month, SEASON_CONFIG.end_day)
    return season_start, season_end


def calculate_season_from_date(game_date: date) -> int:
    """
    Calculate which season a game date belongs to.
    Seasons run from Sep 1 → Jul 30.
    
    Args:
        game_date: Date of the game
        
    Returns:
        Season number (1-indexed)
    """
    # If before September, subtract a year
    if game_date.month < SEASON_CONFIG.start_month:
        season_year = game_date.year - 1
    else:
        season_year = game_date.year
    
    # Calculate season number from first season year
    # This should be adjusted based on when SPL actually started
    # For now, assume Season 1 started in 2022
    first_season_year = 2022
    return (season_year - first_season_year) + 1
