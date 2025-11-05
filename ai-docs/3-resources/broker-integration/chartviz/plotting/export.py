"""Chart export utilities for different output formats."""
from pathlib import Path
from typing import Any, Dict, Optional

import plotly.graph_objects as go

from ..utils.logging import log_export, log_error


class ChartExporter:
    """Handles chart export to various formats."""
    
    def __init__(self, fig: go.Figure):
        """Initialize exporter with Plotly figure."""
        self.fig = fig
        
    def to_html(
        self, 
        file_path: str | Path,
        include_plotlyjs: str = "cdn",
        config: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> None:
        """Export chart to HTML file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            default_config = {
                "displayModeBar": True,
                "displaylogo": False,
                "modeBarButtonsToRemove": ["lasso2d", "select2d"]
            }
            
            if config:
                default_config.update(config)
                
            self.fig.write_html(
                str(path),
                include_plotlyjs=include_plotlyjs,
                config=default_config,
                **kwargs
            )
            
            log_export("HTML", path)
            
        except Exception as e:
            log_error(f"Failed to export HTML to {file_path}", e)
            raise
            
    def to_png(
        self,
        file_path: str | Path,
        width: int = 1200,
        height: int = 600,
        scale: int = 2,
        **kwargs
    ) -> None:
        """Export chart to PNG file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            self.fig.write_image(
                str(path),
                format="png",
                width=width,
                height=height,
                scale=scale,
                **kwargs
            )
            
            log_export("PNG", path)
            
        except Exception as e:
            log_error(f"Failed to export PNG to {file_path}", e)
            raise
            
    def to_jpeg(
        self,
        file_path: str | Path,
        width: int = 1200,
        height: int = 600,
        scale: int = 2,
        **kwargs
    ) -> None:
        """Export chart to JPEG file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            self.fig.write_image(
                str(path),
                format="jpeg",
                width=width,
                height=height,
                scale=scale,
                **kwargs
            )
            
            log_export("JPEG", path)
            
        except Exception as e:
            log_error(f"Failed to export JPEG to {file_path}", e)
            raise
            
    def to_pdf(
        self,
        file_path: str | Path,
        width: int = 1200,
        height: int = 600,
        **kwargs
    ) -> None:
        """Export chart to PDF file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            self.fig.write_image(
                str(path),
                format="pdf",
                width=width,
                height=height,
                **kwargs
            )
            
            log_export("PDF", path)
            
        except Exception as e:
            log_error(f"Failed to export PDF to {file_path}", e)
            raise
            
    def to_svg(
        self,
        file_path: str | Path,
        width: int = 1200,
        height: int = 600,
        **kwargs
    ) -> None:
        """Export chart to SVG file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            self.fig.write_image(
                str(path),
                format="svg",
                width=width,
                height=height,
                **kwargs
            )
            
            log_export("SVG", path)
            
        except Exception as e:
            log_error(f"Failed to export SVG to {file_path}", e)
            raise