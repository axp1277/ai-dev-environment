"""Layer management system for organizing chart elements."""
from typing import Any, Dict, List, Optional, Union

from ..models import Box, Indicator, Level, Shade, Trade
from ..utils.logging import log_debug


class LayerManager:
    """Manages layers and z-ordering of chart elements."""
    
    def __init__(self):
        """Initialize layer manager."""
        self.layers: Dict[str, List[Any]] = {
            'background': [],
            'levels': [],
            'boxes': [],
            'indicators': [],
            'shades': [],
            'trades': [],
            'annotations': []
        }
        self.visibility: Dict[str, bool] = {
            'background': True,
            'levels': True,
            'boxes': True,
            'indicators': True,
            'shades': True,
            'trades': True,
            'annotations': True
        }
        
    def add_level(self, level: Level, layer_name: str = 'levels') -> None:
        """Add level to specified layer."""
        self.layers[layer_name].append(level)
        log_debug(f"Added level to layer {layer_name}")
        
    def add_box(self, box: Box, layer_name: str = 'boxes') -> None:
        """Add box to specified layer."""
        self.layers[layer_name].append(box)
        log_debug(f"Added box to layer {layer_name}")
        
    def add_indicator(self, indicator: Indicator, layer_name: str = 'indicators') -> None:
        """Add indicator to specified layer."""
        self.layers[layer_name].append(indicator)
        log_debug(f"Added indicator {indicator.name} to layer {layer_name}")
        
    def add_shade(self, shade: Shade, layer_name: str = 'shades') -> None:
        """Add shade to specified layer."""
        self.layers[layer_name].append(shade)
        log_debug(f"Added shade to layer {layer_name}")
        
    def add_trade(self, trade: Trade, layer_name: str = 'trades') -> None:
        """Add trade to specified layer."""
        self.layers[layer_name].append(trade)
        log_debug(f"Added trade to layer {layer_name}")
        
    def toggle_layer_visibility(self, layer_name: str) -> bool:
        """Toggle visibility of a layer."""
        if layer_name in self.visibility:
            self.visibility[layer_name] = not self.visibility[layer_name]
            log_debug(f"Toggled layer {layer_name} visibility to {self.visibility[layer_name]}")
            return self.visibility[layer_name]
        return False
        
    def set_layer_visibility(self, layer_name: str, visible: bool) -> None:
        """Set visibility of a layer."""
        if layer_name in self.visibility:
            self.visibility[layer_name] = visible
            log_debug(f"Set layer {layer_name} visibility to {visible}")
            
    def get_layer_elements(self, layer_name: str) -> List[Any]:
        """Get all elements in a specific layer."""
        return self.layers.get(layer_name, [])
        
    def get_visible_layers(self) -> Dict[str, List[Any]]:
        """Get all elements from visible layers."""
        visible = {}
        for layer_name, elements in self.layers.items():
            if self.visibility.get(layer_name, True):
                visible[layer_name] = elements
        return visible
        
    def clear_layer(self, layer_name: str) -> None:
        """Clear all elements from a layer."""
        if layer_name in self.layers:
            count = len(self.layers[layer_name])
            self.layers[layer_name].clear()
            log_debug(f"Cleared {count} elements from layer {layer_name}")
            
    def get_layer_count(self, layer_name: str) -> int:
        """Get count of elements in a layer."""
        return len(self.layers.get(layer_name, []))
        
    def get_total_elements(self) -> int:
        """Get total count of all elements."""
        return sum(len(elements) for elements in self.layers.values())
        
    def list_layers(self) -> Dict[str, Dict[str, Union[int, bool]]]:
        """List all layers with their stats."""
        layer_info = {}
        for layer_name in self.layers:
            layer_info[layer_name] = {
                'count': self.get_layer_count(layer_name),
                'visible': self.visibility.get(layer_name, True)
            }
        return layer_info