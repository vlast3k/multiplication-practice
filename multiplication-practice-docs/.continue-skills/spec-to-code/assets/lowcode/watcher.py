"""
File watcher for low-code editor.
Monitors Python source and JSON config files for changes.
"""
import os
import time
import threading
from pathlib import Path
from typing import Callable, Optional, Set
from dataclasses import dataclass


@dataclass
class WatchState:
    """Tracks file modification times."""
    path: str
    mtime: float = 0.0
    
    def has_changed(self) -> bool:
        """Check if file has been modified since last check."""
        try:
            current_mtime = os.path.getmtime(self.path)
            if current_mtime > self.mtime:
                self.mtime = current_mtime
                return True
        except OSError:
            pass
        return False


class FileWatcher:
    """
    Watches files for changes and triggers callbacks.
    Uses polling for cross-platform compatibility.
    """
    
    def __init__(self, poll_interval: float = 0.5):
        self.poll_interval = poll_interval
        self._watches: dict[str, WatchState] = {}
        self._callbacks: dict[str, list[Callable]] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
    
    def watch(self, path: str, callback: Callable[[], None]) -> None:
        """Add a file to watch with a callback."""
        path = str(Path(path).resolve())
        
        with self._lock:
            if path not in self._watches:
                self._watches[path] = WatchState(path=path)
                # Initialize mtime
                try:
                    self._watches[path].mtime = os.path.getmtime(path)
                except OSError:
                    pass
                self._callbacks[path] = []
            
            self._callbacks[path].append(callback)
    
    def unwatch(self, path: str) -> None:
        """Stop watching a file."""
        path = str(Path(path).resolve())
        
        with self._lock:
            self._watches.pop(path, None)
            self._callbacks.pop(path, None)
    
    def start(self) -> None:
        """Start the watcher thread."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop the watcher thread."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
    
    def _poll_loop(self) -> None:
        """Main polling loop."""
        while self._running:
            with self._lock:
                for path, state in list(self._watches.items()):
                    if state.has_changed():
                        callbacks = self._callbacks.get(path, [])
                        for callback in callbacks:
                            try:
                                callback()
                            except Exception as e:
                                print(f"Watcher callback error for {path}: {e}")
            
            time.sleep(self.poll_interval)


# Global watcher instance
_watcher: Optional[FileWatcher] = None


def get_watcher() -> FileWatcher:
    """Get or create the global watcher instance."""
    global _watcher
    if _watcher is None:
        _watcher = FileWatcher()
    return _watcher


def start_watcher(
    source_path: Optional[str] = None,
    config_path: Optional[str] = None,
    on_source_change: Optional[Callable] = None,
    on_config_change: Optional[Callable] = None,
) -> FileWatcher:
    """
    Start watching files with optional callbacks.
    Blocks until interrupted.
    """
    watcher = get_watcher()
    
    if source_path and on_source_change:
        watcher.watch(source_path, on_source_change)
        print(f"Watching source: {source_path}")
    
    if config_path and on_config_change:
        watcher.watch(config_path, on_config_change)
        print(f"Watching config: {config_path}")
    
    watcher.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        watcher.stop()
    
    return watcher


class ChangeNotifier:
    """
    Collects change notifications and broadcasts to listeners.
    Used by the server to notify WebSocket clients.
    """
    
    def __init__(self):
        self._listeners: Set[Callable[[str, dict], None]] = set()
        self._lock = threading.Lock()
    
    def add_listener(self, callback: Callable[[str, dict], None]) -> None:
        """Add a listener for change notifications."""
        with self._lock:
            self._listeners.add(callback)
    
    def remove_listener(self, callback: Callable[[str, dict], None]) -> None:
        """Remove a listener."""
        with self._lock:
            self._listeners.discard(callback)
    
    def notify(self, event_type: str, data: dict) -> None:
        """Broadcast a change notification to all listeners."""
        with self._lock:
            listeners = list(self._listeners)
        
        for listener in listeners:
            try:
                listener(event_type, data)
            except Exception as e:
                print(f"Notifier callback error: {e}")


# Global notifier instance
_notifier: Optional[ChangeNotifier] = None


def get_notifier() -> ChangeNotifier:
    """Get or create the global notifier instance."""
    global _notifier
    if _notifier is None:
        _notifier = ChangeNotifier()
    return _notifier
