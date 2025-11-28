"""
Event constructor wrappers for Module 2.
"""

from .utils import emit_event
from typing import Dict, Any

def emit_access_request(pid:int, mode:str, segment:int, segment_offset:int, access_type:str):
    ev = {
        "type": "access_request",
        "pid": pid,
        "mode": mode,
        "segment": segment,
        "segment_offset": segment_offset,
        "access_type": access_type
    }
    emit_event(ev)
    return ev

def emit_segment_alloc(pid:int, segment:int, base:int, limit:int, allocator:str):
    ev = {
        "type": "segment_alloc",
        "pid": pid,
        "segment": segment,
        "base": base,
        "limit": limit,
        "allocator": allocator
    }
    emit_event(ev)
    return ev

def emit_seg_translate(pid:int, segment:int, segment_offset:int, status:str, virtual_page=None, page_offset=None, phys_addr=None):
    ev = {
        "type": "seg_translate",
        "pid": pid,
        "segment": segment,
        "segment_offset": segment_offset,
        "status": status
    }
    if virtual_page is not None:
        ev["virtual_page"] = virtual_page
    if page_offset is not None:
        ev["page_offset"] = page_offset
    if phys_addr is not None:
        ev["phys_addr"] = phys_addr
    emit_event(ev)
    return ev

def emit_seg_fault(pid:int, segment:int, segment_offset:int):
    ev = {"type": "seg_fault", "pid": pid, "segment": segment, "segment_offset": segment_offset}
    emit_event(ev)
    return ev

def emit_page_load_request(pid:int, global_page:int, reason:str):
    ev = {"type": "page_load_request", "pid": pid, "global_page": global_page, "reason": reason}
    emit_event(ev)
    return ev

def emit_demand_page_loaded(pid:int, global_page:int, frame:int):
    ev = {"type": "demand_page_loaded", "pid": pid, "global_page": global_page, "frame": frame}
    emit_event(ev)
    return ev
