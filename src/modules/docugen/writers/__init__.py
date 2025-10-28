"""
Output Writers

Utilities for saving documentation outputs as JSON.

DEPRECATED: This module has been moved to docugen.shared.writers.
Imports here are provided for backward compatibility.
"""

import warnings

warnings.warn(
    "Importing from 'docugen.writers' is deprecated. "
    "Use 'docugen.shared.writers' instead.",
    DeprecationWarning,
    stacklevel=2
)

from ..shared.writers.json_writer import save_layer_outputs

__all__ = ["save_layer_outputs"]
