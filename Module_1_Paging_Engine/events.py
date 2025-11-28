"""
Event helper wrappers for Module 1. These create structured event dicts
and call utils.emit_event().

All functions return the dict they emitted for in-process use.
"""

from .utils import emit_event
from typing import Dict, Any

def emit_page_fault(pid: int, page: int) -> Dict[str, Any]:
    ev = {"type": "page_fault", "pid": pid, "page": page}
    emit_event(ev)
    return ev

def emit_page_in(pid: int, global_page: int, frame: int) -> Dict[str, Any]:
    ev = {"type": "page_in", "pid": pid, "global_page": global_page, "frame": frame}
    emit_event(ev)
    return ev

def emit_page_out(pid: int, global_page: int, frame: int) -> Dict[str, Any]:
    ev = {"type": "page_out", "pid": pid, "global_page": global_page, "frame": frame}
    emit_event(ev)
    return ev

def emit_page_load_request(pid: int, global_page: int, reason: str) -> Dict[str, Any]:
    ev = {"type": "page_load_request", "pid": pid, "global_page": global_page, "reason": reason}
    emit_event(ev)
    return ev