"""
Small associative TLB implementation with event emissions for tlb_hit / tlb_miss.

The TLB maps virtual page -> frame (global_page -> frame).
On lookup, emits 'tlb_hit' or 'tlb_miss'.
"""

from typing import Dict, Optional, Tuple
from .utils import emit_event

class TLB:
    def __init__(self, size: int = 8):
        
        self.size = size
        self.store: Dict[int, int] = {}  # gpage -> frame
        self.order: List[int] = []

    def lookup(self, pid: int, gpage: int) -> Optional[int]:
        if gpage in self.store:
            ev = {"type": "tlb_hit", "pid": pid, "global_page": gpage}
            emit_event(ev)
            # update LRU-like order
            if gpage in self.order:
                self.order.remove(gpage)
                self.order.append(gpage)
            return self.store[gpage]
        else:
            ev = {"type": "tlb_miss", "pid": pid, "global_page": gpage}
            emit_event(ev)
            return None

    def insert(self, pid: int, gpage: int, frame: int):
        if gpage in self.store:
            self.order.remove(gpage)
        elif len(self.store) >= self.size:
            # evict least recently used
            victim = self.order.pop(0)
            del self.store[victim]
        self.store[gpage] = frame
        self.order.append(gpage)