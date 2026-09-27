"""
utils.py - Path and Directory Utilities for the Economic Data Pipeline.

This module centralizes all path management using Python's standard `pathlib`
library so that file paths work seamlessly across Windows, macOS, and Linux
without any hardcoded absolute paths.
"""

from pathlib import Path
from typing import Dict


def get_project_root() -> Path:
    """
    Returns the absolute path to the project root directory.
    
    Assumes this file is located in <project_root>/python/utils.py.
    Using .resolve() ensures symbolic links and relative references are resolved.
    """
    return Path(__file__).resolve().parent.parent


def get_pipeline_paths() -> Dict[str, Path]:
    """
    Returns a dictionary of all standard directory paths used across the pipeline.
    
    Returns:
        dict: Mapping of folder keys to Path objects.
    """
    root = get_project_root()
    return {
        "root": root,
        "data_raw": root / "data" / "raw",
        "data_processed": root / "data" / "processed",
        "notebooks": root / "notebooks",
        "python": root / "python",
        "r": root / "R",
        "outputs_figures": root / "outputs" / "figures",
        "outputs_tables": root / "outputs" / "tables",
        "docs": root / "docs",
    }


def ensure_directories_exist() -> None:
    """
    Verifies that all required project directories exist.
    Creates any missing directories automatically.
    """
    paths = get_pipeline_paths()
    for name, path in paths.items():
        if name != "root" and not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"[INIT] Created directory: {path.relative_to(paths['root'])}")


def print_step_banner(step_number: int, step_name: str, description: str) -> None:
    """
    Prints a clear, formatted banner in the console for each pipeline step.
    Helps college students clearly follow and explain execution during a viva.
    
    Args:
        step_number (int): Step number in the pipeline.
        step_name (str): Short title of the step.
        description (str): Brief 1-line description of the step's objective.
    """
    separator = "=" * 65
    print(f"\n{separator}")
    print(f" STEP {step_number}: {step_name.upper()}")
    print(f" {description}")
    print(f"{separator}\n")


if __name__ == "__main__":
    # Test path resolution and directory verification
    print("Testing utils.py path resolution...")
    root_path = get_project_root()
    print(f"Project Root: {root_path}")
    
    ensure_directories_exist()
    all_paths = get_pipeline_paths()
    for key, p in all_paths.items():
        status = "OK" if p.exists() else "MISSING"
        print(f" - {key:16s} : {p.name}/ [{status}]")
    print("\nUtils test completed successfully.")
