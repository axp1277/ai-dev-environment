"""Level line configuration model."""
from typing import Literal

from pydantic import BaseModel, Field


class Level(BaseModel):
    """Horizontal or angled level line configuration."""
    price: float = Field(..., description="Price level")
    start_bar: int = Field(..., description="Starting bar index")
    end_bar: int | None = Field(None, description="Ending bar index (None for current)")
    color: str = Field("#ffeb3b", description="Line color")
    width: float = Field(2, description="Line width")
    dash: Literal["solid", "dot", "dash", "longdash", "dashdot"] = Field("solid")
    opacity: float = Field(0.8, ge=0, le=1, description="Line opacity")
    label: str | None = Field(None, description="Optional label text")
    extend_right: bool = Field(True, description="Extend to current bar")
    show_price_label: bool = Field(False, description="Show price label at line end")
    label_position: Literal["right", "left"] = Field("right", description="Label position")
    label_bg_color: str | None = Field(None, description="Label background color")
    label_font_color: str = Field("#000000", description="Label font color")
    label_font_size: int = Field(12, description="Label font size")
    
    class Config:
        validate_assignment = True