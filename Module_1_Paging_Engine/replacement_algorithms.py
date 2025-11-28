"""
Replacement algorithms: FIFO, LRU, Clock.

Interfaces are minimal to be used by PhysicalMemory above.
"""

from typing import Optional, Tuple, Dict, List

class FIFOReplacer:
    def __init__(self, frames_count):
        self.queue: List[int] = []
        self.frame_to_page: Dict[int, Optional[int]] = {}

    def add(self, frame: int, gpage: int):
        self.queue.append(frame)
        self.frame_to_page[frame] = gpage

    def pick_victim(self) -> Tuple[int, int]:
        if not self.queue:
            raise RuntimeError("No frames to evict")
        victim = self.queue.pop(0)
        page = self.frame_to_page.get(victim)
        return victim, page

    def replace(self, frame: int, gpage: int):
        # append the new frame to queue
        self.queue.append(frame)
        self.frame_to_page[frame] = gpage

    def touch(self, frame: int, gpage: int):
        # FIFO ignores touch
        pass

    def remove(self, frame: int):
        if frame in self.queue:
            self.queue.remove(frame)
        self.frame_to_page.pop(frame, None)

class LRUReplacer:
    def __init__(self, frames_count):
        self.order: List[int] = []
        self.frame_to_page: Dict[int, Optional[int]] = {}

    def add(self, frame: int, gpage: int):
        if frame in self.order:
            self.order.remove(frame)
        self.order.append(frame)
        self.frame_to_page[frame] = gpage

    def pick_victim(self) -> Tuple[int, int]:
        if not self.order:
            raise RuntimeError("No frames to evict")
        victim = self.order.pop(0)
        return victim, self.frame_to_page.get(victim)

    def replace(self, frame: int, gpage: int):
        # touched frame becomes most recently used
        if frame in self.order:
            self.order.remove(frame)
        self.order.append(frame)
        self.frame_to_page[frame] = gpage

    def touch(self, frame: int, gpage: int):
        if frame in self.order:
            self.order.remove(frame)
        self.order.append(frame)

    def remove(self, frame: int):
        if frame in self.order:
            self.order.remove(frame)
        self.frame_to_page.pop(frame, None)

class ClockReplacer:
    def __init__(self, frames_count):
        self.frames: List[Optional[int]] = [None] * frames_count
        self.use_bits: Dict[int, int] = {}
        self.pointer = 0

    def add(self, frame: int, gpage: int):
        self.frames[frame] = gpage
        self.use_bits[frame] = 1

    def pick_victim(self) -> Tuple[int, int]:
        n = len(self.frames)
        for _ in range(2*n):
            idx = self.pointer % n
            if self.use_bits.get(idx, 0) == 0:
                victim = idx
                self.pointer = (idx + 1) % n
                return victim, self.frames[victim]
            else:
                self.use_bits[idx] = 0
            self.pointer = (self.pointer + 1) % n
        # fallback: choose pointer
        victim = self.pointer % n
        return victim, self.frames[victim]

    def replace(self, frame: int, gpage: int):
        self.frames[frame] = gpage
        self.use_bits[frame] = 1
        self.pointer = (frame + 1) % len(self.frames)

    def touch(self, frame: int, gpage: int):
        self.use_bits[frame] = 1

    def remove(self, frame: int):
        self.frames[frame] = None
        self.use_bits.pop(frame, None)
        