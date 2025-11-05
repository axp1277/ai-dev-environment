"""Configuration merger for combining default and user configurations."""
from typing import Any, Dict, List, Optional, Union

from ..utils.logging import log_debug


class ConfigMerger:
    """Handles merging of configuration dictionaries with advanced strategies."""
    
    def __init__(self, merge_strategy: str = "deep"):
        """Initialize merger with specified strategy."""
        self.merge_strategy = merge_strategy
        
    def merge(self, base: Dict[str, Any], override: Dict[str, Any], 
              strategy: Optional[str] = None) -> Dict[str, Any]:
        """Merge configurations using specified strategy."""
        strategy = strategy or self.merge_strategy
        
        if strategy == "deep":
            return self._deep_merge(base, override)
        elif strategy == "shallow":
            return self._shallow_merge(base, override)
        elif strategy == "replace":
            return self._replace_merge(base, override)
        else:
            raise ValueError(f"Unknown merge strategy: {strategy}")
            
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge configurations recursively."""
        result = base.copy()
        
        for key, value in override.items():
            if key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._deep_merge(result[key], value)
                elif isinstance(result[key], list) and isinstance(value, list):
                    result[key] = self._merge_lists(result[key], value)
                else:
                    result[key] = value
            else:
                result[key] = self._deep_copy_value(value)
                
        log_debug(f"Deep merged configs with {len(override)} overrides")
        return result
        
    def _shallow_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Shallow merge - only top-level keys."""
        result = base.copy()
        result.update(override)
        log_debug(f"Shallow merged configs with {len(override)} overrides")
        return result
        
    def _replace_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Replace merge - override completely replaces base."""
        log_debug("Replaced base config with override")
        return override.copy()
        
    def _merge_lists(self, base_list: List[Any], override_list: List[Any], 
                     list_strategy: str = "replace") -> List[Any]:
        """Merge two lists based on strategy."""
        if list_strategy == "replace":
            return override_list.copy()
        elif list_strategy == "extend":
            result = base_list.copy()
            result.extend(override_list)
            return result
        elif list_strategy == "merge":
            # For lists of dicts, try to merge by matching keys
            if all(isinstance(item, dict) for item in base_list + override_list):
                return self._merge_dict_lists(base_list, override_list)
            else:
                return override_list.copy()
        else:
            return override_list.copy()
            
    def _merge_dict_lists(self, base_list: List[Dict], override_list: List[Dict]) -> List[Dict]:
        """Merge lists of dictionaries by matching keys."""
        result = base_list.copy()
        
        for override_item in override_list:
            # Try to find matching item by 'name' or 'id' key
            match_key = self._find_match_key(override_item)
            if match_key:
                matched = False
                for i, base_item in enumerate(result):
                    if (match_key in base_item and 
                        base_item[match_key] == override_item[match_key]):
                        result[i] = self._deep_merge(base_item, override_item)
                        matched = True
                        break
                        
                if not matched:
                    result.append(override_item.copy())
            else:
                result.append(override_item.copy())
                
        return result
        
    def _find_match_key(self, item: Dict[str, Any]) -> Optional[str]:
        """Find key to use for matching in dict lists."""
        match_keys = ['name', 'id', 'key', 'type']
        for key in match_keys:
            if key in item:
                return key
        return None
        
    def _deep_copy_value(self, value: Any) -> Any:
        """Deep copy a value recursively."""
        if isinstance(value, dict):
            return {k: self._deep_copy_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._deep_copy_value(item) for item in value]
        else:
            return value
            
    def merge_multiple(self, configs: List[Dict[str, Any]], 
                      strategy: Optional[str] = None) -> Dict[str, Any]:
        """Merge multiple configurations in order."""
        if not configs:
            return {}
            
        result = configs[0].copy()
        
        for config in configs[1:]:
            result = self.merge(result, config, strategy)
            
        log_debug(f"Merged {len(configs)} configurations")
        return result
        
    def create_override_config(self, base: Dict[str, Any], 
                              overrides: Dict[str, Any]) -> Dict[str, Any]:
        """Create a configuration that only contains overrides."""
        override_config = {}
        
        for key, value in overrides.items():
            if key in base:
                if isinstance(base[key], dict) and isinstance(value, dict):
                    nested_override = self.create_override_config(base[key], value)
                    if nested_override:
                        override_config[key] = nested_override
                elif base[key] != value:
                    override_config[key] = value
            else:
                override_config[key] = value
                
        return override_config
        
    def validate_merge_compatibility(self, config1: Dict[str, Any], 
                                   config2: Dict[str, Any]) -> List[str]:
        """Check for potential merge conflicts and return warnings."""
        warnings = []
        
        for key in config1.keys() & config2.keys():
            val1, val2 = config1[key], config2[key]
            
            if type(val1) != type(val2):
                warnings.append(f"Type mismatch for key '{key}': {type(val1)} vs {type(val2)}")
            elif isinstance(val1, dict) and isinstance(val2, dict):
                nested_warnings = self.validate_merge_compatibility(val1, val2)
                warnings.extend([f"{key}.{w}" for w in nested_warnings])
                
        return warnings