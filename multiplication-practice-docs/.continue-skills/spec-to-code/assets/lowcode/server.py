"""
FastAPI server with WebSocket support for the low-code editor.
"""
import asyncio
import json
import os
from pathlib import Path
from typing import Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class ConfigUpdate(BaseModel):
    """Configuration update payload."""
    config: dict


class ConnectionManager:
    """Manages WebSocket connections for broadcasting updates."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: dict):
        """Send message to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.active_connections.discard(conn)


def create_app(
    source_path: Optional[str] = None,
    config_path: Optional[str] = None,
    watch: bool = True,
) -> FastAPI:
    """Create the FastAPI application."""
    
    app = FastAPI(title="Low-Code Agent Editor")
    manager = ConnectionManager()
    
    # Store paths in app state
    app.state.source_path = source_path
    app.state.config_path = config_path or "agent_config.json"
    app.state.manager = manager
    
    # Find editor.html - check multiple locations
    editor_paths = [
        Path(__file__).parent.parent.parent.parent / "lowcode-editor" / "editor.html",
        Path(__file__).parent / "editor.html",
        Path.cwd() / "editor.html",
    ]
    
    editor_html_path = None
    for p in editor_paths:
        if p.exists():
            editor_html_path = p
            break
    
    @app.get("/")
    async def serve_editor():
        """Serve the editor HTML with no caching."""
        from fastapi.responses import Response
        if editor_html_path and editor_html_path.exists():
            with open(editor_html_path, 'r') as f:
                content = f.read()
            return Response(
                content=content,
                media_type="text/html",
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0"
                }
            )
        
        # Fallback: return a basic message
        return HTMLResponse("""
        <html>
            <body>
                <h1>Low-Code Editor</h1>
                <p>Editor HTML not found. Please ensure editor.html is in the correct location.</p>
            </body>
        </html>
        """)
    
    @app.get("/api/config")
    async def get_config():
        """Get current configuration."""
        config_file = Path(app.state.config_path)
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        
        # Return default config if file doesn't exist
        return {
            "name": "",
            "model": "",
            "description": "",
            "temperature": 0.7,
            "prompts": {},
            "tools": [],
            "mcpServers": [],
        }
    
    @app.post("/api/config")
    async def save_config(update: ConfigUpdate):
        """Save configuration and broadcast update."""
        config_file = Path(app.state.config_path)
        
        # Ensure directory exists
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write config
        with open(config_file, 'w') as f:
            json.dump(update.config, f, indent=2)
        
        # Broadcast to all connected clients
        await manager.broadcast({
            "type": "config.saved",
            "config": update.config,
        })
        
        return {"status": "ok", "message": "Configuration saved"}
    
    @app.get("/api/status")
    async def get_status():
        """Get server status."""
        return {
            "status": "running",
            "source_path": app.state.source_path,
            "config_path": app.state.config_path,
            "connections": len(manager.active_connections),
        }
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket endpoint for real-time updates."""
        await manager.connect(websocket)
        
        try:
            # Send initial config on connect
            config_file = Path(app.state.config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                await websocket.send_json({
                    "type": "config.initial",
                    "config": config,
                })
            
            # Keep connection alive and handle messages
            while True:
                try:
                    data = await asyncio.wait_for(
                        websocket.receive_json(),
                        timeout=30.0
                    )
                    
                    # Handle client messages
                    if data.get("type") == "ping":
                        await websocket.send_json({"type": "pong"})
                    
                    elif data.get("type") == "config.update":
                        # Client wants to save config
                        config = data.get("config", {})
                        config_file = Path(app.state.config_path)
                        
                        with open(config_file, 'w') as f:
                            json.dump(config, f, indent=2)
                        
                        # Broadcast to other clients
                        for conn in manager.active_connections:
                            if conn != websocket:
                                try:
                                    await conn.send_json({
                                        "type": "config.updated",
                                        "config": config,
                                    })
                                except Exception:
                                    pass
                        
                        await websocket.send_json({
                            "type": "config.saved",
                            "config": config,
                        })
                
                except asyncio.TimeoutError:
                    # Send keepalive ping
                    try:
                        await websocket.send_json({"type": "keepalive"})
                    except Exception:
                        break
        
        except WebSocketDisconnect:
            pass
        finally:
            manager.disconnect(websocket)
    
    # Set up file watcher if enabled
    if watch and (source_path or config_path):
        @app.on_event("startup")
        async def start_file_watcher():
            from .watcher import get_watcher, get_notifier
            
            watcher = get_watcher()
            notifier = get_notifier()
            
            # Watch config file for external changes
            if config_path:
                def on_config_change():
                    # Schedule async broadcast
                    asyncio.create_task(broadcast_config_change())
                
                watcher.watch(config_path, on_config_change)
            
            # Watch source file for decorator changes
            if source_path:
                def on_source_change():
                    from .cli import extract_decorators_from_file
                    
                    # Re-extract decorators
                    config = extract_decorators_from_file(source_path)
                    
                    # Merge with existing config
                    config_file = Path(app.state.config_path)
                    if config_file.exists():
                        with open(config_file, 'r') as f:
                            existing = json.load(f)
                        for key, value in config.items():
                            if value:
                                existing[key] = value
                        config = existing
                    
                    # Save updated config
                    with open(config_file, 'w') as f:
                        json.dump(config, f, indent=2)
                    
                    # Schedule broadcast
                    asyncio.create_task(broadcast_config_change())
                
                watcher.watch(source_path, on_source_change)
            
            watcher.start()
            print(f"File watcher started")
        
        async def broadcast_config_change():
            """Broadcast config change to all WebSocket clients."""
            config_file = Path(app.state.config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                await manager.broadcast({
                    "type": "config.updated",
                    "config": config,
                })
        
        @app.on_event("shutdown")
        async def stop_file_watcher():
            from .watcher import get_watcher
            watcher = get_watcher()
            watcher.stop()
            print(f"File watcher stopped")
    
    return app


def run_server(app: FastAPI, host: str = "127.0.0.1", port: int = 8080):
    """Run the server with uvicorn."""
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="info")


# CLI entry point
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Low-Code Editor Server")
    parser.add_argument("-c", "--config", default="agent_config.json", help="Config file path")
    parser.add_argument("-s", "--source", help="Python source file to watch")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Server port")
    parser.add_argument("-H", "--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--no-watch", dest="watch", action="store_false", help="Disable file watching")
    
    args = parser.parse_args()
    
    app = create_app(
        source_path=args.source,
        config_path=args.config,
        watch=args.watch,
    )
    
    run_server(app, host=args.host, port=args.port)
