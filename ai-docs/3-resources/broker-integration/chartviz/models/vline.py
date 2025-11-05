"""Vertical line configuration model."""
from typing import Literal

from pydantic import BaseModel, Field


class VLine(BaseModel):
    """Vertical line configuration spanning the full y-axis."""
    bar_index: int = Field(..., description="Bar index for vertical line position")
    color: str = Field("#ff0000", description="Line color")
    width: float = Field(2, description="Line width")
    dash: Literal["solid", "dot", "dash", "longdash", "dashdot"] = Field("solid")
    opacity: float = Field(0.8, ge=0, le=1, description="Line opacity")
    label: str | None = Field(None, description="Optional label text")
    show_label: bool = Field(False, description="Show label at top of line")
    label_position: Literal["top", "bottom"] = Field("top", description="Label position")
    label_bg_color: str | None = Field(None, description="Label background color")
    label_font_color: str = Field("#000000", description="Label font color")
    label_font_size: int = Field(12, description="Label font size")
    
    class Config:
        validate_assignment = True