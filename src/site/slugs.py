"""
Player Name and Slug Utilities
Generates display names and URL-safe slugs for players.
"""

import re
import unicodedata
from typing import Dict, Tuple


def generate_display_name(full_name: str) -> str:
    """
    Generate display name: first name + surname initial.
    
    Special cases:
    - Nicknames like "Mantino (Basile)" or "Coyote (Cri)" → keep as-is
    - Single names → return as-is
    
    Args:
        full_name: Full player name
        
    Returns:
        Display name (e.g., "Cameron M." or "Mantino (Basile)")
    
    Examples:
        >>> generate_display_name("Cameron McAinsh")
        'Cameron M.'
        >>> generate_display_name("Mantino (Basile)")
        'Mantino (Basile)'
        >>> generate_display_name("Coyote (Cri)")
        'Coyote (Cri)'
    """
    # Check if it's a nickname (contains parentheses)
    if '(' in full_name and ')' in full_name:
        return full_name.strip()
    
    # Split into parts
    parts = full_name.strip().split()
    
    # If single name, return as-is
    if len(parts) == 1:
        return parts[0]
    
    # First name + surname initial
    first_name = parts[0]
    surname = parts[-1]
    surname_initial = surname[0].upper() if surname else ''
    
    return f"{first_name} {surname_initial}."


def generate_slug(name: str) -> str:
    """
    Generate URL-safe slug from player name.
    
    Args:
        name: Player name (can be display name or full name)
        
    Returns:
        URL-safe slug (lowercase, hyphenated)
    
    Examples:
        >>> generate_slug("Cameron M.")
        'cameron-m'
        >>> generate_slug("Mantino (Basile)")
        'mantino-basile'
        >>> generate_slug("José María")
        'jose-maria'
    """
    # Normalize unicode characters (remove accents)
    slug = unicodedata.normalize('NFKD', name)
    slug = slug.encode('ascii', 'ignore').decode('ascii')
    
    # Remove parentheses but keep content
    slug = re.sub(r'[()]', '', slug)
    
    # Convert to lowercase
    slug = slug.lower()
    
    # Replace spaces and dots with hyphens
    slug = re.sub(r'[\s.]+', '-', slug)
    
    # Remove any non-alphanumeric characters (except hyphens)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    
    # Strip leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug


def generate_player_names(players: list) -> Dict[str, Dict[str, str]]:
    """
    Generate display names and slugs for all players.
    
    Args:
        players: List of full player names
        
    Returns:
        Dict mapping full name to {'display_name': str, 'slug': str}
    
    Example:
        >>> generate_player_names(['Cameron McAinsh', 'Mantino (Basile)'])
        {
            'Cameron McAinsh': {
                'display_name': 'Cameron M.',
                'slug': 'cameron-m'
            },
            'Mantino (Basile)': {
                'display_name': 'Mantino (Basile)',
                'slug': 'mantino-basile'
            }
        }
    """
    result = {}
    
    for player in players:
        display_name = generate_display_name(player)
        slug = generate_slug(display_name)
        
        result[player] = {
            'display_name': display_name,
            'slug': slug,
            'full_name': player
        }
    
    return result


def ensure_unique_slugs(player_names: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """
    Ensure all slugs are unique by adding numbers to duplicates.
    
    Args:
        player_names: Dict from generate_player_names()
        
    Returns:
        Updated dict with unique slugs
    """
    slug_counts: Dict[str, int] = {}
    slug_mapping: Dict[str, str] = {}
    
    # First pass: count slug occurrences
    for full_name, data in player_names.items():
        slug = data['slug']
        slug_counts[slug] = slug_counts.get(slug, 0) + 1
    
    # Second pass: add numbers to duplicates
    slug_usage: Dict[str, int] = {}
    
    for full_name, data in player_names.items():
        slug = data['slug']
        
        if slug_counts[slug] > 1:
            # This slug appears multiple times
            usage = slug_usage.get(slug, 0) + 1
            slug_usage[slug] = usage
            
            # Add number suffix
            unique_slug = f"{slug}-{usage}"
            player_names[full_name]['slug'] = unique_slug
    
    return player_names
