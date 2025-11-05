"""Candlestick chart configuration model."""
from pydantic import BaseModel, Field


class Candlestick(BaseModel):
    """Candlestick visual properties configuration."""
    increasing_line_color: str = Field("#26a69a", description="Bullish candle outline color")
    increasing_fillcolor: str = Field("#26a69a", description="Bullish candle fill color")
    decreasing_line_color: str = Field("#ef5350", description="Bearish candle outline color")
    decreasing_fillcolor: str = Field("#ef5350", description="Bearish candle fill color")
    line_width: float = Field(1, description="Candle outline width")
    whiskerwidth: float = Field(0, description="Wick width ratio (0-1)")
    opacity: float = Field(1.0, ge=0, le=1, description="Candle opacity")
    
    class Config:
        validate_assignment = True