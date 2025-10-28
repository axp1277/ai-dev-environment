"""
DocuGen - Multi-agent Code Documentation Generator

This module provides tools for automatically generating comprehensive
documentation for codebases using LLM-powered agents.
"""

import warnings


def __getattr__(name):
    """
    Provide backward-compatible imports with deprecation warnings.

    This allows existing code to continue working while migrating to the new structure.
    """
    # Map old module names to new locations
    module_mappings = {
        "orchestrator": "docugen.workflows.llm_first.orchestrator",
        "state": "docugen.workflows.llm_first.state",
        "core": "docugen.shared.core",
        "logger": "docugen.shared.logger",
    }

    if name in module_mappings:
        new_path = module_mappings[name]
        warnings.warn(
            f"Importing '{name}' from 'docugen' is deprecated. "
            f"Use '{new_path}' instead.",
            DeprecationWarning,
            stacklevel=2
        )

        # Dynamically import and return the module
        import importlib
        parts = new_path.split('.')
        module = importlib.import_module(new_path)
        return module

    raise AttributeError(f"module 'docugen' has no attribute '{name}'")


__version__ = "0.2.0"
__all__ = []
