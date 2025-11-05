"""Box/Rectangle configuration model."""
from typing import Literal

from pydantic import BaseModel, Field


class Box(BaseModel):
    """Rectangle/box overlay configuration."""
    x0: int = Field(..., description="Starting bar index")
    x1: int | None = Field(None, description="Ending bar index (None for current)")
    y0: float = Field(..., description="Bottom price level")
    y1: float = Field(..., description="Top price level")
    fillcolor: str = Field("rgba(33, 150, 243, 0.2)", description="Fill color")
    line_color: str = Field("#2196f3", description="Border color")
    line_width: float = Field(2, description="Border width")
    line_dash: Literal["solid", "dot", "dash", "longdash", "dashdot"] = Field("solid")
    opacity: float = Field(0.5, ge=0, le=1, description="Fill opacity")
    layer: Literal["below", "above"] = Field("below", description="Layer position")
    label: str | None = Field(None, description="Optional label text")
    
    class Config:
        validate_assignment = True