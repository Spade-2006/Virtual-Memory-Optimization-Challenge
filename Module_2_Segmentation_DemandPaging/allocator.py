"""
SimpleAllocator: deterministic first_fit, best_fit, worst_fit and free/merge.

The allocator manages an address space (0 .. space_size-1) and tracks allocated blocks.
Blocks are represented as (base, size). Merging occurs on free.
"""

from typing import List, Tuple, Optional

class SimpleAllocator:
    def __init__(self, space_size: int):
        self.space_size = space_size
        # maintain free list as list of (base, size) sorted by base
        self.free: List[Tuple[int, int]] = [(0, space_size)]
        # allocated map: base -> size
        self.allocated = {}

    def _merge_free(self):
        self.free.sort()
        merged = []
        for base, size in self.free:
            if not merged:
                merged.append((base, size))
            else:
                last_base, last_size = merged[-1]
                if last_base + last_size == base:
                    merged[-1] = (last_base, last_size + size)
                else:
                    merged.append((base, size))
        self.free = merged

    def first_fit(self, size: int) -> Optional[int]:
        for i, (base, sz) in enumerate(self.free):
            if sz >= size:
                alloc_base = base
                self.allocated[alloc_base] = size
                # shrink or remove
                if sz == size:
                    self.free.pop(i)
                else:
                    self.free[i] = (base + size, sz - size)
                return alloc_base
        return None

    def best_fit(self, size: int) -> Optional[int]:
        best_i = None
        best_sz = None
        for i, (base, sz) in enumerate(self.free):
            if sz >= size:
                if best_sz is None or sz < best_sz:
                    best_sz = sz
                    best_i = i
        if best_i is None:
            return None
        base, sz = self.free[best_i]
        alloc_base = base
        self.allocated[alloc_base] = size
        if sz == size:
            self.free.pop(best_i)
        else:
            self.free[best_i] = (base + size, sz - size)
        return alloc_base

    def worst_fit(self, size: int) -> Optional[int]:
        worst_i = None
        worst_sz = -1
        for i, (base, sz) in enumerate(self.free):
            if sz >= size and sz > worst_sz:
                worst_sz = sz
                worst_i = i
        if worst_i is None:
            return None
        base, sz = self.free[worst_i]
        alloc_base = base
        self.allocated[alloc_base] = size
        if sz == size:
            self.free.pop(worst_i)
        else:
            self.free[worst_i] = (base + size, sz - size)
        return alloc_base

    def free_block(self, base: int) -> bool:
        size = self.allocated.pop(base, None)
        if size is None:
            return False
        self.free.append((base, size))
        self._merge_free()
        return True
