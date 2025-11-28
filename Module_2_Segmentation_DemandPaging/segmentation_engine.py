"""
SegmentationEngine supports create_segment and seg_translate.

Modes:
- 'pure-seg': returns physical address (base + offset) for simplicity
- 'segmented-paging': returns virtual_page and page_offset and uses global page registry
"""

from typing import Tuple
from .allocator import SimpleAllocator
from .global_page_registry import GlobalPageRegistry
from . import events as ev

PAGE_SIZE = 4096

class SegmentationEngine:
    def __init__(self, address_space_size=1<<20, allocator_algo="first_fit"):
        self.allocator = SimpleAllocator(address_space_size)
        self.registry = GlobalPageRegistry()
        # segments: (pid, seg_id) -> (base, size_bytes)
        self.segments = {}
        self.allocator_algo = allocator_algo

    def create_segment(self, pid: int, seg_id: int, size_bytes: int):
        # round up to PAGE_SIZE for segment-size convenience
        size = ((size_bytes + PAGE_SIZE - 1) // PAGE_SIZE) * PAGE_SIZE
        if self.allocator_algo == "first_fit":
            base = self.allocator.first_fit(size)
        elif self.allocator_algo == "best_fit":
            base = self.allocator.best_fit(size)
        else:
            base = self.allocator.worst_fit(size)
        if base is None:
            raise MemoryError("Allocation failed")
        limit = size
        self.segments[(pid, seg_id)] = (base, limit)
        ev.emit_segment_alloc(pid, seg_id, base, limit, self.allocator_algo)
        # register pages in this segment deterministically
        page_count = limit // PAGE_SIZE
        for page_in_seg in range(page_count):
            self.registry.reserve(pid, seg_id, page_in_seg)
        return {"base": base, "limit": limit}

    def seg_translate(self, pid: int, seg_id: int, offset: int, mode="segmented-paging"):
        entry = self.segments.get((pid, seg_id))
        if entry is None:
            ev.emit_seg_fault(pid, seg_id, offset)
            raise Exception("Segment not found")
        base, limit = entry
        if offset < 0 or offset >= limit:
            ev.emit_seg_fault(pid, seg_id, offset)
            raise Exception("Offset out of bounds")
        if mode == "pure-seg":
            phys = base + offset
            ev.emit_seg_translate(pid, seg_id, offset, status="ok", phys_addr=phys)
            return {"status": "ok", "phys_addr": phys}
        elif mode == "segmented-paging":
            page_in_seg = offset // PAGE_SIZE
            page_offset = offset % PAGE_SIZE
            global_page = self.registry.lookup(pid, seg_id, page_in_seg)
            ev.emit_seg_translate(pid, seg_id, offset, status="ok", virtual_page=global_page, page_offset=page_offset)
            return {"status": "ok", "virtual_page": global_page, "page_offset": page_offset}
        else:
            ev.emit_seg_fault(pid, seg_id, offset)
            raise Exception("Unknown translation mode")
