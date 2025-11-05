"""Trade visualization configuration models."""
from typing import Literal

from pydantic import BaseModel, Field


class Marker(BaseModel):
    """Trade marker configuration."""
    symbol: Literal[
        "circle", "square", "diamond", "cross", "x",
        "triangle-up", "triangle-down", "triangle-left", "triangle-right",
        "pentagon", "hexagon", "star", "arrow-up", "arrow-down"
    ] = Field("triangle-up")
    size: int = Field(12, description="Marker size")
    color: str = Field("#4caf50", description="Marker color")
    line_width: float = Field(0, description="Marker outline width")
    line_color: str = Field("#000000", description="Marker outline color")


class ConnectionLine(BaseModel):
    """Trade connection line configuration."""
    color: str = Field("#9e9e9e", description="Line color")
    width: float = Field(1, description="Line width")
    dash: Literal["solid", "dot", "dash", "longdash", "dashdot"] = Field("dash")
    opacity: float = Field(0.7, ge=0, le=1, description="Line opacity")


class Trade(BaseModel):
    """Trade visualization configuration."""
    entry_bar: int = Field(..., description="Entry bar index")
    entry_price: float = Field(..., description="Entry price")
    exit_bar: int = Field(..., description="Exit bar index")
    exit_price: float = Field(..., description="Exit price")
    entry_marker: Marker = Field(default_factory=lambda: Marker())
    exit_marker: Marker = Field(default_factory=lambda: Marker(symbol="triangle-down", color="#f44336"))
    connection_line: ConnectionLine = Field(default_factory=ConnectionLine)
    show_pnl: bool = Field(False, description="Show P&L annotation")
    label: str | None = Field(None, description="Trade label")
    
    class Config:
        validate_assignment = True