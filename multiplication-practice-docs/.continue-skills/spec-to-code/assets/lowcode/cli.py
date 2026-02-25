"""
Low-Code Agent Editor CLI

Commands:
    sync   - Extract decorators from Python file to JSON
    serve  - Start editor server with file watching
    watch  - Watch for changes and auto-sync
"""
import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def extract_decorators_from_file(filepath: str) -> Dict[str, Any]:
    """
    Parse a Python file and extract lowcode decorator configurations.
    Returns a config dict ready for JSON serialization.
    """
    with open(filepath, 'r') as f:
        source = f.read()
    
    tree = ast.parse(source)
    config: Dict[str, Any] = {
        'name': '',
        'model': '',
        'description': '',
        'temperature': 0.7,
        'prompts': {},
        'tools': [],
        'mcpServers': [],
        'exposedParams': []
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check for lowcode decorators
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    dec_config = _parse_decorator(decorator, node)
                    if dec_config:
                        _merge_config(config, dec_config)
    
    return config


def _get_function_return_value(func_node: ast.FunctionDef) -> Any:
    """Extract the return value from a simple function."""
    for stmt in func_node.body:
        if isinstance(stmt, ast.Return) and stmt.value:
            try:
                return ast.literal_eval(stmt.value)
            except (ValueError, TypeError):
                # For string concatenation or complex expressions
                if isinstance(stmt.value, ast.Constant):
                    return stmt.value.value
                # Try to get the raw source
                pass
    return None


def _parse_decorator(decorator: ast.Call, func_node: ast.FunctionDef) -> Optional[Dict[str, Any]]:
    """Parse a single decorator call and extract its configuration."""
    # Get decorator name
    if isinstance(decorator.func, ast.Name):
        name = decorator.func.id
    elif isinstance(decorator.func, ast.Attribute):
        name = decorator.func.attr
    else:
        return None
    
    # Only process known decorators
    if name not in ('agent_config', 'prompt_section', 'mcp_server', 'exposed_param'):
        return None
    
    # Extract arguments
    args = []
    kwargs = {}
    
    for arg in decorator.args:
        args.append(_eval_ast_literal(arg))
    
    for keyword in decorator.keywords:
        if keyword.arg:  # Skip **kwargs
            kwargs[keyword.arg] = _eval_ast_literal(keyword.value)
    
    # Get the return value from the decorated function
    return_value = _get_function_return_value(func_node)
    
    # Map to config structure based on decorator type
    if name == 'agent_config':
        key = kwargs.get('key', args[0] if args else '')
        return {
            'type': 'agent_config',
            'key': key,
            'label': kwargs.get('label', ''),
            'description': kwargs.get('description', ''),
            'value': return_value,
        }
    
    elif name == 'prompt_section':
        key = kwargs.get('key', args[0] if args else 'system')
        return {
            'type': 'prompt',
            'key': key,
            'label': kwargs.get('label', ''),
            'description': kwargs.get('description', ''),
            'content': return_value if return_value else '',
        }
    
    elif name == 'mcp_server':
        key = kwargs.get('key', args[0] if args else '')
        # Return value should be a dict with command, args, etc.
        mcp_config = return_value if isinstance(return_value, dict) else {}
        return {
            'type': 'mcp_server',
            'key': key,
            'label': kwargs.get('label', ''),
            'description': kwargs.get('description', ''),
            'command': mcp_config.get('command', kwargs.get('command', '')),
            'args': mcp_config.get('args', kwargs.get('args', [])),
            'env': mcp_config.get('env', kwargs.get('env', {})),
        }
    
    elif name == 'exposed_param':
        key = kwargs.get('key', args[0] if args else '')
        return {
            'type': 'exposed_param',
            'key': key,
            'label': kwargs.get('label', ''),
            'description': kwargs.get('description', ''),
        }
    
    return None


def _eval_ast_literal(node: ast.expr) -> Any:
    """Safely evaluate an AST node to a Python literal."""
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        # For complex expressions, return string representation
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            # Handle things like GroupKind.BASICS
            return f"{_eval_ast_literal(node.value)}.{node.attr}"
        return None


def _merge_config(config: Dict, decorator_config: Dict) -> None:
    """Merge decorator config into the main config."""
    dec_type = decorator_config.get('type')
    key = decorator_config.get('key', '')
    
    if dec_type == 'agent_config':
        value = decorator_config.get('value')
        # Handle dotted key paths like "agent.model"
        if key.startswith('agent.'):
            field = key.split('.')[-1]
            if field == 'model' and value:
                config['model'] = value
            elif field == 'temperature' and value is not None:
                config['temperature'] = value
            elif field == 'name' and value:
                config['name'] = value
            elif field == 'description' and value:
                config['description'] = value
        elif key == 'name' and value:
            config['name'] = value
        elif key == 'model' and value:
            config['model'] = value
    
    elif dec_type == 'prompt':
        content = decorator_config.get('content', '')
        # Handle dotted key paths like "prompts.system"
        prompt_key = key.split('.')[-1] if '.' in key else key
        config['prompts'][prompt_key] = content
    
    elif dec_type == 'mcp_server':
        server_name = key.split('.')[-1] if '.' in key else key
        config['mcpServers'].append({
            'name': server_name,
            'label': decorator_config.get('label', ''),
            'description': decorator_config.get('description', ''),
            'command': decorator_config.get('command', ''),
            'args': decorator_config.get('args', []),
            'env': decorator_config.get('env', {}),
        })
    
    elif dec_type == 'exposed_param':
        config['exposedParams'].append({
            'key': key,
            'label': decorator_config.get('label', ''),
            'description': decorator_config.get('description', ''),
        })


def cmd_sync(args: argparse.Namespace) -> int:
    """Extract decorators from Python file and save to JSON."""
    source_path = Path(args.source)
    
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}", file=sys.stderr)
        return 1
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = source_path.parent / 'agent_config.json'
    
    # Extract configuration
    print(f"Extracting decorators from: {source_path}")
    config = extract_decorators_from_file(str(source_path))
    
    # Merge with existing config if present
    if output_path.exists() and not args.force:
        print(f"Merging with existing config: {output_path}")
        with open(output_path, 'r') as f:
            existing = json.load(f)
        # Only overwrite fields that were extracted (non-empty)
        for key, value in config.items():
            if value or key not in existing:
                existing[key] = value
        config = existing
    
    # Write output
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Saved configuration to: {output_path}")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    """Start the editor server with file watching."""
    try:
        from .server import create_app, run_server
    except ImportError:
        from server import create_app, run_server
    
    source_path = Path(args.source) if args.source else None
    config_path = Path(args.config) if args.config else None
    
    # Auto-detect config path
    if source_path and not config_path:
        config_path = source_path.parent / 'agent_config.json'
    
    print(f"Starting editor server on http://localhost:{args.port}")
    if source_path:
        print(f"Watching: {source_path}")
    if config_path:
        print(f"Config: {config_path}")
    
    app = create_app(
        source_path=str(source_path) if source_path else None,
        config_path=str(config_path) if config_path else None,
        watch=args.watch,
    )
    
    run_server(app, host=args.host, port=args.port)
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    """Watch for file changes and auto-sync."""
    try:
        from .watcher import start_watcher
    except ImportError:
        from watcher import start_watcher
    
    source_path = Path(args.source)
    config_path = Path(args.config) if args.config else source_path.parent / 'agent_config.json'
    
    print(f"Watching for changes:")
    print(f"  Source: {source_path}")
    print(f"  Config: {config_path}")
    print("Press Ctrl+C to stop.")
    
    start_watcher(
        source_path=str(source_path),
        config_path=str(config_path),
        on_source_change=lambda: cmd_sync(argparse.Namespace(
            source=str(source_path),
            output=str(config_path),
            force=False,
        )),
    )
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog='lowcode',
        description='Low-Code Agent Editor CLI',
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # sync command
    sync_parser = subparsers.add_parser('sync', help='Extract decorators to JSON')
    sync_parser.add_argument('source', help='Python source file with decorators')
    sync_parser.add_argument('-o', '--output', help='Output JSON file (default: agent_config.json)')
    sync_parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing config')
    
    # serve command
    serve_parser = subparsers.add_parser('serve', help='Start editor server')
    serve_parser.add_argument('source', nargs='?', help='Python source file to watch')
    serve_parser.add_argument('-c', '--config', help='JSON config file')
    serve_parser.add_argument('-p', '--port', type=int, default=8080, help='Server port')
    serve_parser.add_argument('-H', '--host', default='127.0.0.1', help='Server host')
    serve_parser.add_argument('--no-watch', dest='watch', action='store_false', help='Disable file watching')
    
    # watch command
    watch_parser = subparsers.add_parser('watch', help='Watch and auto-sync')
    watch_parser.add_argument('source', help='Python source file to watch')
    watch_parser.add_argument('-c', '--config', help='JSON config file')
    
    args = parser.parse_args(argv)
    
    if args.command == 'sync':
        return cmd_sync(args)
    elif args.command == 'serve':
        return cmd_serve(args)
    elif args.command == 'watch':
        return cmd_watch(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
