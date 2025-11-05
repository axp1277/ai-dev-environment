"""Theme management system for ChartViz."""
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .loader import ConfigLoader
from .merger import ConfigMerger
from ..utils.logging import log_debug, log_error, log_warning


class Theme:
    """Represents a chart theme with metadata and configuration."""
    
    def __init__(self, name: str, config: Dict[str, Any], 
                 description: str = "", file_path: Optional[Path] = None):
        """Initialize theme."""
        self.name = name
        self.description = description
        self.config = config
        self.file_path = file_path
        
    @classmethod
    def from_file(cls, file_path: Path) -> "Theme":
        """Load theme from YAML file."""
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            
        name = data.pop('name', file_path.stem)
        description = data.pop('description', '')
        
        return cls(name=name, config=data, description=description, file_path=file_path)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'config': self.config,
            'file_path': str(self.file_path) if self.file_path else None
        }
        
    def save(self, file_path: Path) -> None:
        """Save theme to file."""
        data = self.config.copy()
        data['name'] = self.name
        data['description'] = self.description
        
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)
            
        self.file_path = file_path
        log_debug(f"Saved theme '{self.name}' to {file_path}")


class ThemeRegistry:
    """Manages themes and theme operations."""
    
    def __init__(self, themes_dir: Optional[Path] = None):
        """Initialize theme registry."""
        if themes_dir is None:
            self.themes_dir = Path(__file__).parent / "themes"
        else:
            self.themes_dir = Path(themes_dir)
            
        self.themes: Dict[str, Theme] = {}
        self.config_loader = ConfigLoader()
        self.config_merger = ConfigMerger()
        
        self._load_builtin_themes()
        
    def _load_builtin_themes(self) -> None:
        """Load built-in themes from themes directory."""
        if not self.themes_dir.exists():
            log_warning(f"Themes directory not found: {self.themes_dir}")
            return
            
        for theme_file in self.themes_dir.glob("*.yaml"):
            try:
                theme = Theme.from_file(theme_file)
                self.themes[theme.name] = theme
                log_debug(f"Loaded theme: {theme.name}")
            except Exception as e:
                log_error(f"Error loading theme from {theme_file}", e)
                
    def get_theme(self, name: str) -> Optional[Theme]:
        """Get theme by name."""
        return self.themes.get(name)
        
    def list_themes(self) -> List[str]:
        """Get list of available theme names."""
        return list(self.themes.keys())
        
    def get_theme_info(self) -> Dict[str, Dict[str, str]]:
        """Get information about all themes."""
        return {
            name: {
                'description': theme.description,
                'file_path': str(theme.file_path) if theme.file_path else 'Built-in'
            }
            for name, theme in self.themes.items()
        }
        
    def register_theme(self, theme: Theme) -> None:
        """Register a new theme."""
        self.themes[theme.name] = theme
        log_debug(f"Registered theme: {theme.name}")
        
    def load_theme_from_file(self, file_path: Path) -> Theme:
        """Load and register theme from file."""
        theme = Theme.from_file(file_path)
        self.register_theme(theme)
        return theme
        
    def create_theme(self, name: str, base_theme: Optional[str] = None,
                    overrides: Optional[Dict[str, Any]] = None,
                    description: str = "") -> Theme:
        """Create a new theme."""
        if base_theme:
            base = self.get_theme(base_theme)
            if not base:
                raise ValueError(f"Base theme '{base_theme}' not found")
            config = base.config.copy()
        else:
            config = self.config_loader.get_default_config()
            
        if overrides:
            config = self.config_merger.merge(config, overrides)
            
        theme = Theme(name=name, config=config, description=description)
        self.register_theme(theme)
        return theme
        
    def apply_theme(self, theme_name: str, base_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Apply theme to base configuration."""
        theme = self.get_theme(theme_name)
        if not theme:
            raise ValueError(f"Theme '{theme_name}' not found")
            
        if base_config is None:
            return theme.config.copy()
            
        return self.config_merger.merge(base_config, theme.config)
        
    def save_theme(self, theme_name: str, file_path: Optional[Path] = None) -> None:
        """Save theme to file."""
        theme = self.get_theme(theme_name)
        if not theme:
            raise ValueError(f"Theme '{theme_name}' not found")
            
        if file_path is None:
            file_path = self.themes_dir / f"{theme.name.lower()}.yaml"
            
        file_path.parent.mkdir(parents=True, exist_ok=True)
        theme.save(file_path)
        
    def delete_theme(self, theme_name: str, delete_file: bool = False) -> bool:
        """Delete theme from registry."""
        if theme_name not in self.themes:
            return False
            
        theme = self.themes[theme_name]
        
        if delete_file and theme.file_path and theme.file_path.exists():
            theme.file_path.unlink()
            log_debug(f"Deleted theme file: {theme.file_path}")
            
        del self.themes[theme_name]
        log_debug(f"Deleted theme: {theme_name}")
        return True
        
    def duplicate_theme(self, source_name: str, new_name: str,
                       description: str = "") -> Theme:
        """Create a duplicate of an existing theme."""
        source_theme = self.get_theme(source_name)
        if not source_theme:
            raise ValueError(f"Source theme '{source_name}' not found")
            
        new_theme = Theme(
            name=new_name,
            config=source_theme.config.copy(),
            description=description or f"Copy of {source_theme.description}"
        )
        
        self.register_theme(new_theme)
        return new_theme
        
    def get_theme_preview(self, theme_name: str) -> Dict[str, Any]:
        """Get a preview of theme settings."""
        theme = self.get_theme(theme_name)
        if not theme:
            raise ValueError(f"Theme '{theme_name}' not found")
            
        preview = {
            'name': theme.name,
            'description': theme.description,
            'colors': {}
        }
        
        config = theme.config
        
        # Extract key colors for preview
        if 'chart_layout' in config:
            layout = config['chart_layout']
            preview['colors']['background'] = layout.get('background_color', '#ffffff')
            preview['colors']['font'] = layout.get('font_color', '#000000')
            
        if 'candlestick' in config:
            candle = config['candlestick']
            preview['colors']['bullish'] = candle.get('increasing_line_color', '#26a69a')
            preview['colors']['bearish'] = candle.get('decreasing_line_color', '#ef5350')
            
        return preview
        
    def validate_theme(self, theme_name: str) -> List[str]:
        """Validate theme configuration and return any errors."""
        theme = self.get_theme(theme_name)
        if not theme:
            return [f"Theme '{theme_name}' not found"]
            
        errors = []
        
        # Validate each configuration section
        for section_name, section_config in theme.config.items():
            if isinstance(section_config, dict):
                is_valid = self.config_loader.validate_config_section(
                    section_config, section_name
                )
                if not is_valid:
                    errors.append(f"Invalid {section_name} configuration")
                    
        return errors