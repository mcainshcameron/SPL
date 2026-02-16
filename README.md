# SPL Platform v2

Static website and data pipeline for the Solo Pro League (SPL).

## Installation

```bash
pip install -e .
```

## Usage

### Process Data
```bash
# Run full pipeline
spl pipeline --input data/input/FantaSPL_Milano.xlsx

# Process with custom output directory
spl pipeline --input data/input/FantaSPL_Milano.xlsx --output output/data
```

### Build Site
```bash
# Build static site from processed data
spl build

# Build with custom paths
spl build --data output/data --output output/site
```

### Development
```bash
# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

## Project Structure

```
spl-platform/
├── src/
│   ├── pipeline/          # Data processing
│   ├── site/             # Site generator
│   ├── templates/        # Jinja2 templates
│   └── static/           # CSS, JS, images
├── data/input/           # Excel input files
├── output/data/          # Processed JSON
├── output/site/          # Built static site
└── tests/               # Unit tests
```

## Data Pipeline

The pipeline processes Excel files containing SPL game data and generates JSON files for the static site:

1. **Processor** - Game and points calculation
2. **Summarizer** - Player rankings and statistics
3. **Market** - EWMA-based market valuations
4. **Fantasy** - Fantasy league standings
5. **News** - Auto-generated SPLNews headlines

## Configuration

All parameters are in `src/pipeline/config.py`:
- Scoring rules per match type
- Market valuation parameters
- Season boundaries
- Championship splits
