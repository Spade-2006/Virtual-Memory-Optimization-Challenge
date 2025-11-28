"""
Utilities for Module 2: uses the same shared tick file & events.log as Module 1.

Implements tick() and emit_event() similar to Module 1 so events share the same timeline.
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
    """Shared tick counter (reads/writes same vm_tick.json as Module 1)."""
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
    """Append event to shared events.log, adding time if absent."""
    _init_tick_file()
    if "time" not in event:
        event["time"] = tick()
    line = json.dumps(event, sort_keys=True)
    with open(_EVENTS_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"[EVENT {event['time']}] {event.get('type', 'unknown')}")
