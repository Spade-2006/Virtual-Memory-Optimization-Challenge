"""
Global page registry maps (pid, seg_id, page_in_seg) -> unique global page id.

Global page ids start at 1 and increment deterministically.
"""

from typing import Tuple, Dict

class GlobalPageRegistry:
    def __init__(self):
        self.map: Dict[Tuple[int,int,int], int] = {}
        self._next = 1

    def reserve(self, pid: int, seg_id: int, page_in_seg: int) -> int:
        key = (pid, seg_id, page_in_seg)
        if key not in self.map:
            self.map[key] = self._next
            self._next += 1
        return self.map[key]

    def lookup(self, pid: int, seg_id: int, page_in_seg: int) -> int:
        key = (pid, seg_id, page_in_seg)
        return self.map.get(key, None)
