"""Chart layout configuration models."""
from typing import Literal

from pydantic import BaseModel, Field


class Margin(BaseModel):
    """Chart margin configuration."""
    l: int = Field(60, description="Left margin")
    r: int = Field(40, description="Right margin")
    t: int = Field(40, description="Top margin")
    b: int = Field(40, description="Bottom margin")


class Axis(BaseModel):
    """Axis configuration for chart."""
    showgrid: bool = Field(True, description="Show grid lines")
    gridcolor: str = Field("#333333", description="Grid line color")
    gridwidth: float = Field(1, description="Grid line width")
    showline: bool = Field(True, description="Show axis line")
    linecolor: str = Field("#444444", description="Axis line color")
    tickcolor: str = Field("#ffffff", description="Tick color")
    side: Literal["left", "right", "top", "bottom"] | None = None


class ChartLayout(BaseModel):
    """Main chart layout configuration."""
    background_color: str = Field("#1e1e1e", description="Background color")
    paper_bgcolor: str = Field("#1e1e1e", description="Paper background color")
    plot_bgcolor: str = Field("#1e1e1e", description="Plot background color")
    font_family: str = Field("Arial, sans-serif", description="Font family")
    font_size: int = Field(12, description="Base font size")
    font_color: str = Field("#ffffff", description="Font color")
    showlegend: bool = Field(False, description="Show legend")
    margin: Margin = Field(default_factory=Margin)
    xaxis: Axis = Field(default_factory=lambda: Axis())
    yaxis: Axis = Field(default_factory=lambda: Axis(side="right"))
    height: int | None = Field(None, description="Chart height in pixels")
    width: int | None = Field(None, description="Chart width in pixels")
    
    class Config:
        validate_assignment = True