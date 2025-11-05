# ChartViz: Financial Chart Visualization Framework

ChartViz is a minimalistic, powerful Python framework for creating highly customizable financial candlestick charts with layered visual elements. Designed for both human developers and AI agents, it provides a CLI-driven, pip-installable package that enables dynamic chart generation with professional-grade visualizations suitable for trading analysis and client presentations.

## 🚀 Quick Start

### Installation

```bash
# Install in development mode from the project root
uv pip install -e .

# Verify installation
chartviz --version
```

### Basic Usage

```bash
# Create a chart from SQLite database
chartviz from-db --symbol AAPL --timeframe 5minute --output chart.html

# Create a chart with Polygon.io data
chartviz from-polygon --symbol TSLA --timeframe 15minute --days 7 --output tsla_chart.html

# Apply a custom theme
chartviz from-db --symbol SPY --theme dark --output spy_dark.html

# Show chart interactively in browser
chartviz from-db --symbol EURUSD --show --output forex.html
```

## 📊 Features

- **Multiple Data Sources**: SQLite database and Polygon.io API integration
- **Professional Themes**: Dark, Light, Classic, and Professional presets
- **Interactive Charts**: HTML output with zoom, pan, and hover capabilities
- **Automatic Browser Opening**: Charts open automatically in your default browser
- **Sequential X-Axis**: No gaps in candlestick charts during weekends/holidays
- **Customizable Layout**: Full control over colors, fonts, and styling
- **CLI and Programmatic API**: Use from command line or Python code

## 🎨 Available Themes

### Dark Theme
- Black background with high contrast
- Bright green/red candles
- Optimal for late-night trading sessions

### Light Theme  
- White background with clean aesthetics
- Traditional blue/red color scheme
- Perfect for presentations and reports

### Classic Theme
- Traditional charting colors
- Balanced contrast for all-day use
- Industry-standard appearance

### Professional Theme
- Corporate-friendly colors
- Suitable for client presentations
- Clean, business-oriented design

## 💻 Command Line Interface

### Global Options

```bash
chartviz [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS]

Global Options:
  -v, --verbose     Enable verbose logging
  -q, --quiet       Suppress output except errors  
  --log-file PATH   Write logs to file
  --help           Show help message
  --version        Show version information
```

### Database Commands

#### `from-db` - Chart from SQLite Database

```bash
chartviz from-db [OPTIONS]

Required Options:
  -s, --symbol TEXT        Symbol to chart (e.g., AAPL, SPY, EURUSD)
  -o, --output TEXT        Output file path (.html)

Optional Options:
  -tf, --timeframe CHOICE  Timeframe [1minute|5minute|15minute|60minute] (default: 5minute)
  -d, --days INTEGER       Days of historical data (default: 5)
  -l, --limit INTEGER      Maximum number of bars
  --db-path TEXT           SQLite database path (default: data/market_data.db)
  --theme TEXT             Chart theme [dark|light|classic|professional]
  --width INTEGER          Chart width in pixels
  --height INTEGER         Chart height in pixels
  --show                   Show chart interactively in browser

Examples:
  chartviz from-db -s AAPL -o apple.html
  chartviz from-db -s SPY -tf 15minute -l 200 -o spy_15min.html --theme dark
  chartviz from-db -s EURUSD --show -o forex.html --width 1400 --height 800
```

#### `from-polygon` - Chart from Polygon.io API

```bash
chartviz from-polygon [OPTIONS]

Required Options:
  -s, --symbol TEXT        Symbol to chart
  -o, --output TEXT        Output file path (.html)

Optional Options:
  -tf, --timeframe CHOICE  Timeframe [1minute|5minute|15minute|60minute|daily] (default: 5minute) 
  -d, --days INTEGER       Days of historical data (default: 5)
  -l, --limit INTEGER      Maximum number of bars
  --theme TEXT             Chart theme
  --width INTEGER          Chart width in pixels
  --height INTEGER         Chart height in pixels
  --show                   Show chart interactively

Examples:
  chartviz from-polygon -s TSLA -d 10 -o tesla.html
  chartviz from-polygon -s /ES -tf 1minute -l 100 -o futures.html --theme professional
```

### Configuration Commands

#### `config` - Configuration Management

```bash
# List all configuration sections
chartviz config list-sections

# Show current default configuration  
chartviz config show

# Create a custom configuration file
chartviz config create my-config.yaml

# Validate a configuration file
chartviz config validate my-config.yaml
```

#### `theme` - Theme Management

```bash
# List available themes
chartviz theme list

# Show theme details
chartviz theme show dark

# Create custom theme from existing one
chartviz theme create my-theme --base dark --output my-theme.yaml
```

## 🐍 Python API

### Basic Programmatic Usage

```python
from chartviz.data import create_provider
from chartviz.plotting import Chart
from chartviz.config import ConfigLoader, ThemeRegistry

# Create data provider
provider = create_provider('sqlite', db_path='data/market_data.db')

# Fetch OHLC data
df = provider.get_ohlc_data('AAPL', '5minute', limit=100)

# Load configuration and theme
config_loader = ConfigLoader()
theme_registry = ThemeRegistry()

base_config = config_loader.get_default_config()
themed_config = theme_registry.apply_theme('dark', base_config)

# Create chart
layout = config_loader.create_chart_layout(themed_config)
chart = Chart(layout, title="AAPL 5-Minute Chart")

# Add candlesticks
candlestick_config = config_loader.create_candlestick(themed_config)
chart.add_candlesticks(df, candlestick_config)

# Export
chart.to_html('aapl_chart.html')
```

### Advanced Usage with Custom Elements

```python
from chartviz.models import Level, Box, Trade

# Add support/resistance levels
support_level = Level(
    price=150.00,
    start_bar=0,
    extend_right=True,
    color="#00ff00",
    width=2,
    label="Support"
)
chart.add_level(support_level)

# Add price boxes/zones
price_zone = Box(
    x0=10,
    y0=149.50,
    x1=90,
    y1=150.50,
    fillcolor="rgba(0, 255, 0, 0.1)",
    line_color="#00ff00"
)
chart.add_box(price_zone)

# Add trade visualization
trade = Trade(
    entry_bar=20,
    entry_price=148.50,
    exit_bar=50,
    exit_price=152.75,
    show_pnl=True
)
chart.add_trade(trade)
```

## 🗂️ Data Sources

### SQLite Database

ChartViz expects SQLite tables with this schema:

```sql
CREATE TABLE {symbol}_{timeframe} (
    timestamp DATETIME PRIMARY KEY,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INTEGER
);

-- Index for performance
CREATE INDEX idx_{symbol}_{timeframe}_timestamp ON {symbol}_{timeframe}(timestamp);
```

**Example table names:**
- `AAPL_5minute`
- `SPY_60minute`
- `EURUSD_15minute`

### Polygon.io API

Requires `POLYGON_API_KEY` environment variable:

```bash
export POLYGON_API_KEY="your_api_key_here"
```

Supports stocks, forex, and futures symbols:
- **Stocks**: `AAPL`, `TSLA`, `SPY`
- **Forex**: `C:EURUSD`, `C:GBPUSD`
- **Futures**: `/ES`, `/NQ`, `/CL`

## ⚙️ Configuration

### Configuration File Structure

```yaml
chart_layout:
  background_color: "#1e1e1e"
  paper_bgcolor: "#1e1e1e"
  plot_bgcolor: "#1e1e1e"
  font_family: "Arial, sans-serif"
  font_size: 12
  font_color: "#ffffff"
  showlegend: false
  margin:
    l: 60
    r: 40
    t: 40
    b: 40
  xaxis:
    showgrid: true
    gridcolor: "#333333"
    gridwidth: 1
  yaxis:
    showgrid: true
    gridcolor: "#333333"
    side: "right"

candlestick:
  increasing_line_color: "#26a69a"
  increasing_fillcolor: "#26a69a"
  decreasing_line_color: "#ef5350"
  decreasing_fillcolor: "#ef5350"
  line_width: 1
  whiskerwidth: 0

level:
  default_color: "#ffeb3b"
  default_width: 2
  default_dash: "solid"
  opacity: 0.8

box:
  default_fillcolor: "rgba(33, 150, 243, 0.2)"
  default_line_color: "#2196f3"
  default_line_width: 2

trade:
  entry_marker:
    symbol: "triangle-up"
    size: 12
    color: "#4caf50"
  exit_marker:
    symbol: "triangle-down"
    size: 12
    color: "#f44336"
```

### Custom Themes

Create custom themes by copying and modifying existing theme files:

```bash
# Copy dark theme as starting point
cp src/chartviz/config/themes/dark.yaml my-custom-theme.yaml

# Edit colors and styling
# Apply with: --theme /path/to/my-custom-theme.yaml
```

## 🔧 Technical Details

### Architecture

```
ChartViz/
├── cli.py              # Single-file CLI with all commands
├── data/               # Data provider implementations
│   ├── base.py        # Abstract DataProvider interface  
│   ├── sqlite.py      # SQLite database provider
│   └── polygon.py     # Polygon.io API provider
├── models/            # Pydantic data models
│   ├── candlestick.py # Candlestick configuration
│   ├── level.py       # Horizontal level lines
│   ├── box.py         # Rectangle overlays
│   └── ...
├── plotting/          # Chart rendering engine
│   ├── chart.py       # Core Chart class with Plotly
│   └── export.py      # Export functionality
├── config/            # Configuration management
│   ├── loader.py      # YAML config loading
│   ├── themes.py      # Theme registry
│   └── themes/        # Built-in theme files
└── utils/            # Logging and utilities
```

### Design Principles

1. **Minimalism**: Every line of code justified, files under 500 lines
2. **DRY**: No code duplication, single source of truth
3. **Type Safety**: Full Pydantic model validation
4. **CLI-First**: Optimized for command-line usage
5. **AI-Friendly**: Clear structure for AI debugging and development

### Chart Features

- **Sequential X-Axis**: Uses integer indices with datetime labels to prevent weekend gaps
- **No Rangeslider**: Disabled by default for cleaner appearance  
- **Auto Browser Open**: HTML files automatically open in default browser
- **Responsive**: Charts adapt to different screen sizes
- **Interactive**: Built-in zoom, pan, hover, and crosshair tools

## 🚨 Common Issues

### Database Connection Errors

```bash
# Ensure database path is correct
chartviz from-db --db-path ./data/market_data.db -s AAPL -o test.html

# Check if table exists
sqlite3 ./data/market_data.db ".tables"
```

### Missing API Keys

```bash
# Set Polygon API key
export POLYGON_API_KEY="your_key"

# Verify it's set
echo $POLYGON_API_KEY
```

### Import Errors

```bash
# Reinstall in development mode
cd /path/to/adwr-module
uv pip install -e .

# Check Python path
python -c "import chartviz; print(chartviz.__file__)"
```

## 📚 Examples

### Create Multiple Charts with Different Themes

```bash
# Create charts for the same symbol with all themes
for theme in dark light classic professional; do
    chartviz from-db -s AAPL -o "aapl_${theme}.html" --theme $theme
done
```

### Batch Chart Generation

```bash
# Chart multiple symbols
symbols=(AAPL TSLA SPY MSFT)
for symbol in "${symbols[@]}"; do
    chartviz from-db -s $symbol -o "${symbol,,}_chart.html" --theme dark
done
```

### High-Resolution Export

```bash
# Create large charts for presentations  
chartviz from-polygon -s SPY -o spy_hires.html \
    --width 1920 --height 1080 --theme professional
```

## 🛠️ Development

### Adding Custom Data Providers

1. Create new provider class inheriting from `DataProvider`
2. Implement required methods: `get_ohlc_data()`, `validate_connection()`
3. Register in `data/__init__.py`

### Adding New Chart Elements

1. Create Pydantic model in `models/`
2. Add rendering method to `plotting/chart.py`
3. Update CLI commands if needed

### Testing

```bash
# Run basic functionality test
chartviz from-db -s TEST_SYMBOL -o test_output.html

# Validate all themes load correctly
chartviz theme list

# Test configuration loading
chartviz config show
```

## 📄 License

This project is part of the ADWR Module trading intelligence system.

## 🤝 Contributing

1. Follow minimalist principles - justify every line of code
2. Keep files under 500 lines for AI debugging capability
3. Use type hints and Pydantic validation
4. Write clear, single-line docstrings
5. Test CLI commands before committing changes

---

For more information, see the main project documentation and specification files in `ai-docs/2-specs/specs-34.md`.