"""
Runtime Utilities for Lowcode Configuration

This module is FROZEN - do not modify.
"""

import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypeVar, Union

import yaml

T = TypeVar("T")


def load_yaml_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Args:
        config_path: Path to the YAML config file

    Returns:
        Dictionary with configuration values
    """
    path = Path(config_path)
    if not path.exists():
        return {}

    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def load_json_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a JSON configuration file.

    Args:
        config_path: Path to the JSON config file

    Returns:
        Dictionary with configuration values
    """
    path = Path(config_path)
    if not path.exists():
        return {}

    with open(path, "r") as f:
        return json.load(f)


def get_nested_value(config: Dict[str, Any], key: str) -> Optional[Any]:
    """
    Get a nested value from a config dictionary using dot notation.

    Args:
        config: Configuration dictionary
        key: Dot-separated key (e.g., "agent.model")

    Returns:
        The value if found, None otherwise
    """
    parts = key.split(".")
    current = config

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None

    return current


def resolve(
    key: str,
    default_func: Callable[[], T],
    config: Dict[str, Any],
    env_prefix: str = "",
) -> T:
    """
    Resolve a configuration value with priority:
    1. Environment variable (if env_prefix is set)
    2. Config file value
    3. Default from decorated function

    Args:
        key: Configuration key (e.g., "agent.model")
        default_func: Function that returns the default value
        config: Configuration dictionary
        env_prefix: Optional prefix for environment variable lookup

    Returns:
        The resolved configuration value
    """
    # Check environment variable first
    if env_prefix:
        env_key = f"{env_prefix}_{key.upper().replace('.', '_')}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return _coerce_type(env_value, default_func())

    # Check config file
    config_value = get_nested_value(config, key)
    if config_value is not None:
        return config_value

    # Fall back to default
    return default_func()


def _coerce_type(value: str, reference: T) -> T:
    """Coerce a string value to match the type of a reference value."""
    if isinstance(reference, bool):
        return value.lower() in ("true", "1", "yes")  # type: ignore
    if isinstance(reference, int):
        return int(value)  # type: ignore
    if isinstance(reference, float):
        return float(value)  # type: ignore
    return value  # type: ignore