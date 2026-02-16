"""SPL Site Generator - Build static site from processed data."""

from .slugs import generate_display_name, generate_slug, generate_player_names

__all__ = [
    'generate_display_name',
    'generate_slug',
    'generate_player_names',
]
