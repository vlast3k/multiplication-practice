"""
Lowcode Configuration Module

This module provides decorators and utilities for making agent configurations
editable via the VS Code Code-Based Agent extension.
"""

from .decorators import prompt_section, agent_config, mcp_server, exposed_param
from .registry import REGISTRY, ExposedField, FieldKind, GroupKind, ValidationRules, register_field, get_field, get_all_fields
from .runtime import resolve, load_yaml_config, load_json_config, get_nested_value

__all__ = [
    # Decorators
    "prompt_section",
    "agent_config", 
    "mcp_server",
    "exposed_param",
    # Registry
    "REGISTRY",
    "ExposedField",
    "FieldKind",
    "GroupKind",
    "ValidationRules",
    "register_field",
    "get_field",
    "get_all_fields",
    # Runtime
    "resolve",
    "load_yaml_config",
    "load_json_config",
    "get_nested_value",
]


def export_schema():
    """Export the REGISTRY to a JSON-serializable dict."""
    result = {
        "name": "",
        "model": "",
        "description": "",
        "temperature": 0.7,
        "prompts": {},
        "tools": [],
        "mcpServers": [],
    }
    
    for key, field in REGISTRY.items():
        if field.kind == FieldKind.CONFIG:
            if key == "name":
                result["name"] = field.default
            elif key == "model":
                result["model"] = field.default
            elif key == "description":
                result["description"] = field.default
            elif key == "temperature":
                result["temperature"] = field.default
        
        elif field.kind == FieldKind.PROMPT:
            result["prompts"][key] = field.default
        
        elif field.kind == FieldKind.MCPSERVER:
            result["mcpServers"].append({
                "name": key,
                "label": field.label,
                "description": field.description,
                **field.default
            })
    
    return result
