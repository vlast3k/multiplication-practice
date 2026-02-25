"""
Registry and Enums for Lowcode Configuration

This module is FROZEN - do not modify.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Callable


class FieldKind(Enum):
    """Kind of configuration field."""
    PROMPT = "prompt_section"
    CONFIG = "agent_config"
    PARAM = "param"
    MCPSERVER = "mcp_server"


class GroupKind(Enum):
    """Grouping categories for configuration fields."""
    BASICS = "basics"
    BEHAVIOR = "behavior"
    ADVANCED = "advanced"
    EXPERTISE = "expertise"
    MCP_SERVER = "mcp_server"


@dataclass
class ValidationRules:
    """Validation rules for a field."""
    format: Optional[str] = None  # "text" | "markdown"
    max_length: Optional[int] = None


@dataclass
class ExposedField:
    """Represents a field exposed for low-code editing."""
    key: str
    kind: FieldKind
    label: str
    description: str = ""
    group: str = GroupKind.BASICS.value
    order: int = 0
    validation: Optional[ValidationRules] = None
    default: Any = None
    getter: Optional[Callable] = None
    source: Optional[Dict[str, str]] = field(default_factory=dict)


# Global registry of all exposed fields
REGISTRY: Dict[str, ExposedField] = {}


def register_field(f: ExposedField) -> None:
    """Register a field in the global registry."""
    REGISTRY[f.key] = f


def get_field(key: str) -> Optional[ExposedField]:
    """Get a field from the registry by key."""
    return REGISTRY.get(key)


def get_all_fields() -> Dict[str, ExposedField]:
    """Get all registered fields."""
    return REGISTRY.copy()
