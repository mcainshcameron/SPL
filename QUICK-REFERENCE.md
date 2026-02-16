# SPL v2 - Quick Reference Card

## 🚀 Rebuild Site

```bash
cd /data/.openclaw/workspace/spl-platform
python3 src/site/builder.py
```

## 🔄 Full Pipeline (if data changes)

```bash
cd /data/.openclaw/workspace/spl-platform
python3 -m src pipeline --input /tmp/FantaSPL_code/Input/FantaSPL_Milano.xlsx
python3 src/site/builder.py
```

## 👀 Preview Locally

```bash
python -m http.server -d /data/.openclaw/workspace/spl-platform/output/site 8000
```

## 📁 Key Locations

- **Source templates:** `src/templates/`
- **CSS:** `src/static/css/styles.css`
- **JavaScript:** `src/static/js/main.js`
- **Builder:** `src/site/builder.py`
- **Pipeline:** `src/__main__.py`
- **Output:** `output/site/`
- **Data:** `output/data/`

## 🎨 Recent Changes (Feb 16, 2026)

1. ✅ Owner names shortened (Ludovico R.)
2. ✅ Latest games first in risultati
3. ✅ Fixed ticker at bottom
4. ✅ Mobile tabs scroll
5. ✅ Charts render correctly
6. ✅ Natural Italian language
7. ✅ Logo cleanup
8. ✅ Clickable team names
9. ✅ Visual polish (animations, gradients, etc.)
10. ✅ **Season filtering on classifica**

## 📊 Data Structure

### players.json
```json
{
  "Bovisa": {
    "Totale": [138 players],
    "Stagione 1": [...],
    "Stagione 2": [...],
    "Stagione 3": [...]
  },
  "Lambrate": {
    "Totale": [64 players],
    "Stagione 3": [...]
  },
  "Combinata": {
    "Totale": [155 players],
    "Stagione 3": [...]
  }
}
```

## 🔧 Common Tasks

### Add new season
1. Update Excel file with new season data
2. Run full pipeline
3. Site will auto-generate new season tabs

### Modify text/language
1. Edit templates in `src/templates/`
2. Run `python3 src/site/builder.py`

### Update styles
1. Edit `src/static/css/styles.css`
2. Run `python3 src/site/builder.py`

### Add new page
1. Create template in `src/templates/`
2. Add builder function in `src/site/builder.py`
3. Add nav link in `base.html`

## 🐛 Troubleshooting

### "No module named 'src'"
```bash
cd /data/.openclaw/workspace/spl-platform
python3 -m src pipeline ...
```

### Charts not rendering
- Check JavaScript console for errors
- Verify date format in market data (YYYY-MM-DD)
- Ensure Lightweight Charts library loaded

### Filters not working
- Check JavaScript console
- Verify data-championship and data-season attributes
- Inspect filter-tab elements

### Mobile overflow
- Check `overflow-x: auto` on `.filter-tabs`
- Verify `flex-wrap: nowrap` on tabs
- Test with Chrome DevTools mobile view

## 📱 Mobile Testing

```bash
# Chrome DevTools
1. F12 → Toggle device toolbar
2. Test: iPhone SE, iPad, Pixel 5
3. Check: Filters scroll, nav works, ticker visible

# Real device
1. Run server: python -m http.server -d output/site 8000
2. Find local IP: ip addr show
3. Visit from phone: http://<IP>:8000
```

## 🎯 Quality Checklist

Before deployment:
- [ ] All pages load without errors
- [ ] Mobile nav works
- [ ] Filters show correct data
- [ ] Charts render
- [ ] Links work (player pages, team rosters)
- [ ] Ticker scrolls
- [ ] Animations smooth
- [ ] No console errors

## 🌐 Italian Glossary

- Campionato = Championship
- Stagione = Season
- Totale = Total
- Classifica = Rankings
- Giocatore = Player
- Partite = Games
- Vittorie = Wins
- Gol = Goals
- Punti = Points

## 💾 Backup

Before major changes:
```bash
cp -r output/site output/site.backup.$(date +%Y%m%d)
```

## 📞 Support

Issues? Check:
1. This reference card
2. COMPLETE-SUMMARY.md (detailed changes)
3. FIX-10-SEASON-FILTER.md (season filter details)
4. FIXES-COMPLETE.md (original fixes)

---

**Last updated:** February 16, 2026  
**Version:** 2.0 (with season filtering)
