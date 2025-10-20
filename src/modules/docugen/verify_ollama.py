"""
Ollama Installation Verification Script

Verifies that Ollama is installed, running, and has the required models available.
"""

import sys
from typing import List, Tuple
import subprocess
import json


def check_ollama_installed() -> bool:
    """Check if Ollama CLI is installed and accessible."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ Ollama installed: {version}")
            return True
        else:
            print("✗ Ollama command found but failed to execute")
            return False
    except FileNotFoundError:
        print("✗ Ollama not found in PATH")
        print("  Install from: https://ollama.ai")
        return False
    except subprocess.TimeoutExpired:
        print("✗ Ollama command timed out")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False


def check_ollama_running() -> bool:
    """Check if Ollama service is running."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Ollama service is running")
            return True
        else:
            print("✗ Ollama service not responding")
            print("  Start with: ollama serve")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Ollama service check timed out")
        return False
    except Exception as e:
        print(f"✗ Error checking Ollama service: {e}")
        return False


def list_installed_models() -> List[str]:
    """Get list of installed Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return []

        # Parse output (skip header line)
        lines = result.stdout.strip().split('\n')[1:]
        models = []
        for line in lines:
            if line.strip():
                # Model name is first column
                model_name = line.split()[0]
                models.append(model_name)

        return models
    except Exception as e:
        print(f"Warning: Could not list models: {e}")
        return []


def check_required_models(required: List[str]) -> Tuple[List[str], List[str]]:
    """
    Check which required models are installed.

    Returns:
        Tuple of (installed_models, missing_models)
    """
    installed = list_installed_models()
    missing = []
    found = []

    for model in required:
        # Check if model or any version variant exists
        if any(m.startswith(model.split(':')[0]) for m in installed):
            found.append(model)
        else:
            missing.append(model)

    return found, missing


def main():
    """Run Ollama verification checks."""
    print("=== Ollama Verification ===\n")

    # Check 1: Ollama installed
    if not check_ollama_installed():
        print("\n❌ Ollama is not installed")
        sys.exit(1)

    print()

    # Check 2: Ollama running
    if not check_ollama_running():
        print("\n❌ Ollama service is not running")
        sys.exit(1)

    print()

    # Check 3: Required models
    print("Checking for required models...")
    required_models = [
        "codellama:7b",
        "codellama:13b"
    ]

    found, missing = check_required_models(required_models)

    if found:
        print(f"✓ Found {len(found)} required model(s):")
        for model in found:
            print(f"  - {model}")

    if missing:
        print(f"\n⚠ Missing {len(missing)} required model(s):")
        for model in missing:
            print(f"  - {model}")
        print("\nTo install missing models, run:")
        for model in missing:
            print(f"  ollama pull {model}")
        print()

    # Check 4: List all available models
    all_models = list_installed_models()
    if all_models:
        print(f"\nAll installed models ({len(all_models)}):")
        for model in all_models:
            print(f"  - {model}")

    print("\n=== Verification Complete ===")

    if missing:
        print("⚠ Some required models are missing")
        sys.exit(1)
    else:
        print("✓ All checks passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
