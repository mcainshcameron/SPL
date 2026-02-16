# SPL v2 Website Fixes - February 16, 2026

## ✅ All Changes Implemented

### 1. Fantasy League Manager Names
- Updated `builder.py` to use `generate_display_name()` from `slugs.py` for owner names
- Owners now display as "FirstName I." instead of full names (e.g., "Ludovico R." instead of "Ludovico Righi")

### 2. Risultati — Latest Games First
- Restructured `build_risultati_page()` to sort games as a flat list by date descending
- Most recent games appear first, regardless of championship or season
- Championship and season filters still work correctly

### 3. SPLNews Ticker Position
- Moved ticker from hero section to fixed position at bottom of viewport
- Desktop: Fixed at very bottom, above footer
- Mobile: Fixed just above bottom navigation bar
- Always visible while scrolling (z-index 90)

### 4. Classifica Mobile — Championship Tabs Overflow
- Added `overflow-x: auto` to `.filter-tabs`
- Added `flex-wrap: nowrap` and `white-space: nowrap` to tabs
- Tabs now scroll horizontally on mobile
- Added custom scrollbar styling
- Reduced tab padding on mobile for better fit

### 5. Player Profile — Market Chart Fix
- Fixed date parsing in chart JavaScript
- Now properly extracts start date from week range "YYYY-MM-DD/YYYY-MM-DD"
- Uses `.split('/')[0]` to get first date for Lightweight Charts

### 6. Language — More Natural Italian
All templates updated with better, more casual Italian:
- "La lega calcistica più competitiva di Milano" → "Il calcetto che conta"
- "Vedi classifica →" → "Classifica →"
- "Valori di mercato aggiornati settimanalmente" → "Valutazioni aggiornate ogni settimana"
- "Storico Valore di Mercato" → "Andamento valore"
- "Registro Partite" → "Storico partite"
- "Nessun dato disponibile" → "Dati non disponibili"
- "Stagione 1 - Archivio" → "Archivio Stagione 1"
- "Classifica Finale" → "Classifica"
- "Rose Complete" → "Le rose"
- "La Stagione 2..." → "La prossima stagione verrà annunciata qui."
- "Prossima Stagione" → "Prossima stagione"
- "Friend Referrals" → "Inviti amici"
- "Top Performer" → "Miglior giocatore"
- Removed "Giocatori" stat from home page

### 7. Logo — Remove Duplicate Text
- Removed `<span>SPL</span>` from desktop nav logo
- Removed `<h1>Solo Pro League</h1>` from hero section
- Logo image is sufficient (already says "SPL Solo Pro League")

### 8. FantaLega — Click Team to See Roster
- Made team names in standings table clickable links
- Links point to anchor IDs on roster cards below
- Format: `#team-{team-name-slug}`
- Added JavaScript to auto-expand and scroll to roster when linked

### 9. Visual Enhancements
All polish items implemented:

**Gradient Glow**
- Hero section has radial gradient overlay with accent color

**Animated Number Counters**
- Stat cards count up from 0 to target value on page load
- Uses `data-count` attribute and JavaScript animation

**Hover Glow Effect**
- Market cards have subtle box-shadow glow on hover
- Uses accent color: `rgba(67, 233, 195, 0.2)`

**Rank Badges**
- Top 3 in classifica get emoji badges (🥇🥈🥉)
- Positioned with CSS pseudo-elements

**Smooth Scroll**
- Added `scroll-behavior: smooth` globally
- Smooth transitions when navigating anchors

**Active Row Highlight**
- Table rows show left border accent on hover
- Transition effect with accent color

**Card Entrance Animations**
- Fade-in-up animation using IntersectionObserver
- Cards appear as you scroll down the page
- Stat cards have staggered animation delays

**Better Mobile Spacing**
- Reduced padding/margins across all components on mobile
- More content fits on screen
- Better use of viewport space

**Sticky Table Headers**
- Rankings/classifica tables have sticky headers
- Headers stay visible when scrolling long tables
- Max height with overflow for long tables

## Files Modified

### Python
- `src/site/builder.py` - Updated fantalega and risultati builders

### Templates
- `src/templates/base.html` - Removed logo text
- `src/templates/home.html` - Language fixes, ticker moved, stat removed
- `src/templates/fantalega.html` - Owner display names, team links, language
- `src/templates/risultati.html` - Flat list structure
- `src/templates/mercato.html` - Language fix
- `src/templates/player.html` - Language fixes, chart date fix

### CSS
- `src/static/css/styles.css` - All visual enhancements added

### JavaScript
- `src/static/js/main.js` - Counter animation, card animations, anchor handling

## Verification

Site built successfully:
- ✅ 155 player pages generated
- ✅ All main pages (home, classifica, mercato, fantalega, risultati)
- ✅ Static assets copied
- ✅ Logo copied

Output location: `/data/.openclaw/workspace/spl-platform/output/site/`

Preview command:
```bash
python -m http.server -d /data/.openclaw/workspace/spl-platform/output/site 8000
```
