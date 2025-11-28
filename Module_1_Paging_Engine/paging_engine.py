"""
Paging engine with PTE dataclass, PagingEngine class, and offline optimal calculator.

- PTE: present, frame, dirty, referenced
- PagingEngine supports FIFO, LRU, CLOCK eviction policies via PhysicalMemory
- handle_page_load_request(...) performs synchronous load/evict and emits events via events.py
"""

from dataclasses import dataclass
from typing import Optional, Dict, Tuple, List
from .physical_memory import PhysicalMemory
from . import events as ev
from .utils import emit_event

@dataclass
class PTE:
    present: bool = False
    frame: Optional[int] = None
    dirty: bool = False
    referenced: bool = False

class PagingEngine:
    def __init__(self, frames_count: int = 4, page_size: int = 4096, policy: str = "FIFO"):
        """
        frames_count: number of physical frames.
        page_size: bytes per page (unused for address math here, but kept for realism).
        policy: "FIFO" | "LRU" | "CLOCK"
        """
        self.page_size = page_size
        self.frames_count = frames_count
        self.policy = policy.upper()
        self.physical = PhysicalMemory(frames_count=frames_count, policy=self.policy)
        # map global_page -> PTE
        self.ptes: Dict[int, PTE] = {}

    def ensure_pte(self, gpage: int) -> PTE:
        if gpage not in self.ptes:
            self.ptes[gpage] = PTE()
        return self.ptes[gpage]

    def is_present(self, gpage: int) -> bool:
        pte = self.ptes.get(gpage)
        return bool(pte and pte.present)

    def handle_page_load_request(self, pid: int, gpage: int, access_type: str = "R") -> Dict:
        """
        Synchronous handler for loading a page into memory.
        Emits page_fault/page_in/page_out as required.
        Returns {"status": "loaded"|"ok", "frame": frame}
        """
        pte = self.ensure_pte(gpage)
        if pte.present:
            # update replacement metadata
            self.physical.touch_frame(pte.frame, gpage)
            # mark referenced/dirty if write
            pte.referenced = True
            if access_type.upper() == "W":
                pte.dirty = True
            return {"status": "ok", "frame": pte.frame}

        # page fault
        ev.emit_page_fault(pid, gpage)

        # allocate frame (may evict)
        victim = self.physical.allocate_frame_for(gpage)
        # if eviction happened, victim is (evicted_frame, evicted_global_page)
        if victim is not None:
            evicted_frame, evicted_page = victim
            # mark victim pte not present
            victim_pte = self.ptes.get(evicted_page)
            if victim_pte:
                if victim_pte.dirty:
                    # write back
                    ev.emit_page_out(pid, evicted_page, evicted_frame)
                victim_pte.present = False
                victim_pte.frame = None
                victim_pte.referenced = False

        # assign frame to new page
        frame = self.physical.set_frame_for(gpage)
        pte.present = True
        pte.frame = frame
        pte.referenced = True
        pte.dirty = (access_type.upper() == "W")
        ev.emit_page_in(pid, gpage, frame)
        return {"status": "loaded", "frame": frame}

    @staticmethod
    def optimal_faults_for_trace(trace_gpages: List[int], frames_count: int) -> int:
        """
        Offline Belady's optimal simulation. Returns number of page faults for given trace.
        """
        frames: Dict[int, None] = {}
        faults = 0
        for i, page in enumerate(trace_gpages):
            if page in frames:
                continue
            faults += 1
            if len(frames) < frames_count:
                frames[page] = None
            else:
                # pick page with farthest next use (or never used again)
                farthest_page = None
                farthest_idx = -1
                for p in list(frames.keys()):
                    next_idx = next((j for j in range(i+1, len(trace_gpages)) if trace_gpages[j] == p), None)
                    if next_idx is None:
                        farthest_page = p
                        break
                    if next_idx > farthest_idx:
                        farthest_idx = next_idx
                        farthest_page = p
                # evict farthest_page
                if farthest_page is not None:
                    del frames[farthest_page]
                frames[page] = None
        return faults