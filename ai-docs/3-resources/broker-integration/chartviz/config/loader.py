"""Configuration loader for YAML files with validation."""
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import ValidationError

from ..models import ChartLayout, Candlestick, Level, Box, Indicator, Shade, Trade
from ..utils.logging import log_debug, log_error, log_warning


class ConfigLoader:
    """Handles loading and parsing YAML configuration files."""
    
    def __init__(self, default_config_path: Optional[Path] = None):
        """Initialize config loader with optional default config path."""
        if default_config_path is None:
            self.default_config_path = Path(__file__).parent / "default.yaml"
        else:
            self.default_config_path = Path(default_config_path)
            
        self.default_config: Dict[str, Any] = {}
        self._load_default_config()
        
    def _load_default_config(self) -> None:
        """Load the default configuration file."""
        try:
            with open(self.default_config_path, 'r') as f:
                self.default_config = yaml.safe_load(f)
            log_debug(f"Loaded default config from {self.default_config_path}")
        except FileNotFoundError:
            log_warning(f"Default config file not found: {self.default_config_path}")
            self.default_config = self._get_fallback_config()
        except yaml.YAMLError as e:
            log_error(f"Error parsing default config YAML", e)
            self.default_config = self._get_fallback_config()
            
    def _get_fallback_config(self) -> Dict[str, Any]:
        """Get minimal fallback configuration."""
        return {
            "chart_layout": {
                "background_color": "#1e1e1e",
                "paper_bgcolor": "#1e1e1e",
                "plot_bgcolor": "#1e1e1e",
                "font_color": "#ffffff"
            },
            "candlestick": {
                "increasing_line_color": "#26a69a",
                "decreasing_line_color": "#ef5350"
            }
        }
        
    def load_config(self, config_path: str | Path) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
                
            if config_data is None:
                log_warning(f"Empty config file: {config_path}")
                return {}
                
            log_debug(f"Loaded config from {config_path}")
            return config_data
            
        except yaml.YAMLError as e:
            log_error(f"Error parsing YAML config file: {config_path}", e)
            raise ValueError(f"Invalid YAML format in {config_path}: {e}")
            
    def save_config(self, config: Dict[str, Any], output_path: str | Path) -> None:
        """Save configuration to YAML file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False, indent=2)
            log_debug(f"Saved config to {output_path}")
            
        except Exception as e:
            log_error(f"Error saving config to {output_path}", e)
            raise
            
    def merge_configs(self, base_config: Dict[str, Any], 
                     override_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two configuration dictionaries recursively."""
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
                
        return merged
        
    def get_default_config(self) -> Dict[str, Any]:
        """Get the default configuration."""
        return self.default_config.copy()
        
    def create_chart_layout(self, config: Optional[Dict[str, Any]] = None) -> ChartLayout:
        """Create ChartLayout from configuration."""
        if config is None:
            config = self.default_config
            
        layout_config = config.get('chart_layout', {})
        
        try:
            return ChartLayout(**layout_config)
        except ValidationError as e:
            log_error("Invalid chart layout configuration", e)
            # Return default layout on validation error
            return ChartLayout()
            
    def create_candlestick(self, config: Optional[Dict[str, Any]] = None) -> Candlestick:
        """Create Candlestick from configuration."""
        if config is None:
            config = self.default_config
            
        candlestick_config = config.get('candlestick', {})
        
        try:
            return Candlestick(**candlestick_config)
        except ValidationError as e:
            log_error("Invalid candlestick configuration", e)
            return Candlestick()
            
    def validate_config_section(self, config_section: Dict[str, Any], 
                               section_name: str) -> bool:
        """Validate a specific configuration section."""
        model_map = {
            'chart_layout': ChartLayout,
            'candlestick': Candlestick,
            'level': Level,
            'box': Box,
            'indicator': Indicator,
            'shade': Shade,
            'trade': Trade
        }
        
        if section_name not in model_map:
            log_warning(f"Unknown config section: {section_name}")
            return False
            
        try:
            model_class = model_map[section_name]
            model_class(**config_section)
            return True
        except ValidationError as e:
            log_error(f"Invalid {section_name} configuration", e)
            return False
            
    def get_config_template(self) -> Dict[str, Any]:
        """Get a template configuration with all available options."""
        return {
            "chart_layout": ChartLayout().model_dump(),
            "candlestick": Candlestick().model_dump(),
            "level": Level(price=100, start_bar=0).model_dump(),
            "box": Box(x0=0, y0=100, y1=110).model_dump(),
            "indicator": Indicator(name="SMA", values=[100]).model_dump(),
            "shade": Shade(indicator1_name="Upper", indicator2_name="Lower").model_dump(),
            "trade": Trade(entry_bar=0, entry_price=100, exit_bar=10, exit_price=105).model_dump()
        }