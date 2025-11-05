"""Shade area configuration model."""
from pydantic import BaseModel, Field


class Shade(BaseModel):
    """Shaded area between two indicators configuration."""
    indicator1_name: str = Field(..., description="First indicator name")
    indicator2_name: str = Field(..., description="Second indicator name")
    fillcolor: str = Field("rgba(156, 39, 176, 0.2)", description="Fill color")
    line_width: float = Field(0, description="Border line width")
    opacity: float = Field(0.2, ge=0, le=1, description="Fill opacity")
    fillmode: str = Field("overlay", description="Fill mode")
    layer: str = Field("below", description="Layer position")
    
    class Config:
        validate_assignment = True