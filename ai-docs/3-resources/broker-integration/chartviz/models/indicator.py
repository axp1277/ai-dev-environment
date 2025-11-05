"""Indicator line configuration model."""
from typing import List, Literal

from pydantic import BaseModel, Field


class Indicator(BaseModel):
    """Technical indicator line configuration."""
    name: str = Field(..., description="Indicator name")
    values: List[float] = Field(..., description="Indicator values")
    color: str = Field("#03a9f4", description="Line color")
    width: float = Field(2, description="Line width")
    mode: Literal["lines", "markers", "lines+markers"] = Field("lines")
    dash: Literal["solid", "dot", "dash", "longdash", "dashdot"] = Field("solid")
    opacity: float = Field(1.0, ge=0, le=1, description="Line opacity")
    visible: bool = Field(True, description="Visibility toggle")
    yaxis: Literal["y", "y2"] = Field("y", description="Y-axis assignment")
    fill: Literal["none", "tozeroy", "tonexty"] | None = Field(None)
    
    class Config:
        validate_assignment = True