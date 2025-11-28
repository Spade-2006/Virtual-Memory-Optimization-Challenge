"""
Utilities for Module 1: deterministic tick counter and emit_event.

Tick counter is shared across the process by storing a small JSON file
'vm_tick.json' in the current working directory. This keeps ticks deterministic
within a run and shared between modules that also use the same scheme.
"""

from typing import Dict, Any
import json
import os
import threading
from datetime import datetime

_TICK_FILE = os.path.join(os.getcwd(), "vm_tick.json")
_EVENTS_LOG = os.path.join(os.getcwd(), "events.log")
_TICK_LOCK = threading.Lock()

def _init_tick_file():
    if not os.path.exists(_TICK_FILE):
        with open(_TICK_FILE, "w") as f:
            json.dump({"tick": 0, "created": datetime.utcnow().isoformat()}, f)

def tick() -> int:
    """Increment and return a shared tick counter (deterministic per process run)."""
    _init_tick_file()
    with _TICK_LOCK:
        with open(_TICK_FILE, "r+") as f:
            data = json.load(f)
            data["tick"] += 1
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            return data["tick"]

def emit_event(event: Dict[str, Any]) -> None:
    """
    Append event as a JSON-line to the shared events.log.
    If 'time' key missing, adds time via tick().
    """
    _init_tick_file()
    if "time" not in event:
        event["time"] = tick()
    # deterministic ordering by writing with newline
    line = json.dumps(event, sort_keys=True)
    # ensure events.log exists and is appended atomically per write
    with open(_EVENTS_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    # Also print short summary for demo visibility
    print(f"[EVENT {event['time']}] {event.get('type', 'unknown')}")