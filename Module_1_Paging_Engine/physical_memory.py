"""
Physical memory manager: frames array, free list, allocation and eviction logic.

Uses replacement algorithms implemented in replacement_algorithms.py.
"""

from typing import Optional, Tuple, Dict
from .replacement_algorithms import FIFOReplacer, LRUReplacer, ClockReplacer

class PhysicalMemory:
    def __init__(self, frames_count: int = 4, policy: str = "FIFO"):
        self.frames_count = frames_count
        # frame -> global_page or None
        self.frames: Dict[int, Optional[int]] = {i: None for i in range(frames_count)}
        self.free_list = list(range(frames_count))
        policy = policy.upper()
        if policy == "FIFO":
            self.replacer = FIFOReplacer(frames_count)
        elif policy == "LRU":
            self.replacer = LRUReplacer(frames_count)
        else:
            self.replacer = ClockReplacer(frames_count)

    def allocate_frame_for(self, gpage: int) -> Optional[Tuple[int, int]]:
        """
        Allocate a frame for gpage. If free frame exists, return None (no eviction).
        If eviction happens, return tuple (evicted_frame, evicted_global_page).
        Also informs replacer of allocation.
        """
        if self.free_list:
            frame = self.free_list.pop(0)
            self.frames[frame] = gpage
            self.replacer.add(frame, gpage)
            return None
        # need to evict
        victim_frame, victim_page = self.replacer.pick_victim()
        # record eviction
        self.frames[victim_frame] = gpage
        self.replacer.replace(victim_frame, gpage)
        return (victim_frame, victim_page)

    def set_frame_for(self, gpage: int) -> int:
        """
        After allocate_frame_for called, set_frame_for returns the frame index
        assigned to gpage (search frames).
        """
        for f, p in self.frames.items():
            if p == gpage:
                return f
        # fallback; shouldn't happen
        raise RuntimeError("Frame not found after allocation")

    def touch_frame(self, frame: int, gpage: int) -> None:
        """
        Notify replacer of an access for replacement policy updates.
        """
        self.replacer.touch(frame, gpage)

    def free_frame(self, frame: int) -> None:
        """
        Free a frame (used by tests).
        """
        self.frames[frame] = None
        if frame not in self.free_list:
            self.free_list.append(frame)
        self.replacer.remove(frame)