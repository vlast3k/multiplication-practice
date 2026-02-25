"""
Decorators for Lowcode Configuration

This module is FROZEN - do not modify.
These decorators are used to expose agent configuration for editing
via the VS Code Code-Based Agent extension.
"""

import functools
from typing import Any, Callable, Optional, TypeVar, Union

from .registry import (
    REGISTRY,
    ExposedField,
    FieldKind,
    GroupKind,
    ValidationRules,
    register_field,
)

T = TypeVar("T")


def prompt_section(
    key: str,
    label: str,
    description: str = "",
    group: Union[GroupKind, str] = GroupKind.BASICS,
    order: int = 0,
    validation: Optional[dict] = None,
) -> Callable[[Callable[[], str]], Callable[[], str]]:
    """
    Decorator to expose a prompt section for editing in the lowcode UI.

    Args:
        key: Unique identifier for this prompt (e.g., "prompts.system")
        label: Human-readable label shown in the UI
        description: Help text explaining what this prompt does
        group: Category grouping (GroupKind enum or string)
        order: Sort order within the group (lower = higher priority)
        validation: Optional validation rules dict

    Example:
        @prompt_section(
            key="prompts.identity",
            label="Agent Identity",
            description="Core identity and role definition",
            group=GroupKind.BASICS,
            order=1
        )
        def get_identity_prompt() -> str:
            return "You are an expert assistant..."
    """
    def decorator(func: Callable[[], str]) -> Callable[[], str]:
        # Resolve group value
        group_value = group.value if isinstance(group, GroupKind) else group
        
        # Create validation rules if provided
        val_rules = None
        if validation:
            val_rules = ValidationRules(
                format=validation.get("format"),
                max_length=validation.get("max_length"),
            )

        # Create and register the field
        field = ExposedField(
            key=key,
            kind=FieldKind.PROMPT,
            label=label,
            description=description,
            group=group_value,
            order=order,
            validation=val_rules,
            default=func(),
            getter=func,
        )
        register_field(field)

        @functools.wraps(func)
        def wrapper() -> str:
            return func()

        return wrapper

    return decorator


def agent_config(
    key: str,
    label: str,
    description: str = "",
    group: Union[GroupKind, str] = GroupKind.BASICS,
    order: int = 0,
) -> Callable[[Callable[[], T]], Callable[[], T]]:
    """
    Decorator to expose an agent configuration value for editing.

    Args:
        key: Unique identifier (e.g., "config.model")
        label: Human-readable label
        description: Help text
        group: Category grouping
        order: Sort order

    Example:
        @agent_config(
            key="config.model",
            label="LLM Model",
            description="The language model powering this agent"
        )
        def get_model_name() -> str:
            return "sap/gpt-4o"
    """
    def decorator(func: Callable[[], T]) -> Callable[[], T]:
        group_value = group.value if isinstance(group, GroupKind) else group

        field = ExposedField(
            key=key,
            kind=FieldKind.CONFIG,
            label=label,
            description=description,
            group=group_value,
            order=order,
            default=func(),
            getter=func,
        )
        register_field(field)

        @functools.wraps(func)
        def wrapper() -> T:
            return func()

        return wrapper

    return decorator


def mcp_server(
    key: str,
    label: str,
    description: str = "",
    order: int = 0,
) -> Callable[[Callable[[], dict]], Callable[[], dict]]:
    """
    Decorator to expose an MCP server configuration.

    Args:
        key: Unique identifier (e.g., "mcp.filesystem")
        label: Human-readable label
        description: Help text
        order: Sort order

    Example:
        @mcp_server(
            key="mcp.filesystem",
            label="Filesystem Server",
            description="MCP server for file operations"
        )
        def get_fs_server() -> dict:
            return {"command": "npx", "args": ["-y", "@anthropic/mcp-fs"]}
    """
    def decorator(func: Callable[[], dict]) -> Callable[[], dict]:
        field = ExposedField(
            key=key,
            kind=FieldKind.MCPSERVER,
            label=label,
            description=description,
            group=GroupKind.MCP_SERVER.value,
            order=order,
            default=func(),
            getter=func,
        )
        register_field(field)

        @functools.wraps(func)
        def wrapper() -> dict:
            return func()

        return wrapper

    return decorator


def exposed_param(
    key: str,
    label: str,
    description: str = "",
    group: Union[GroupKind, str] = GroupKind.ADVANCED,
    order: int = 0,
) -> Callable[[Callable[[], T]], Callable[[], T]]:
    """
    Decorator to expose a runtime parameter for editing.

    Args:
        key: Unique identifier
        label: Human-readable label
        description: Help text
        group: Category grouping
        order: Sort order

    Example:
        @exposed_param(
            key="params.max_tokens",
            label="Max Tokens",
            description="Maximum tokens in response"
        )
        def get_max_tokens() -> int:
            return 4096
    """
    def decorator(func: Callable[[], T]) -> Callable[[], T]:
        group_value = group.value if isinstance(group, GroupKind) else group

        field = ExposedField(
            key=key,
            kind=FieldKind.PARAM,
            label=label,
            description=description,
            group=group_value,
            order=order,
            default=func(),
            getter=func,
        )
        register_field(field)

        @functools.wraps(func)
        def wrapper() -> T:
            return func()

        return wrapper

    return decorator