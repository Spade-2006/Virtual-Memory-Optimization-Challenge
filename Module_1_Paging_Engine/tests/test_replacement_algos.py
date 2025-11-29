import pytest
from Module_1_Paging_Engine.replacement_algorithms import FIFOReplacer, LRUReplacer, ClockReplacer

def test_fifo_basic():
    r = FIFOReplacer(3)
    r.add(0, 100); r.add(1, 101); r.add(2, 102)
    victim, page = r.pick_victim()
    assert victim == 0

def test_lru_touch_order():
    r = LRUReplacer(3)
    r.add(0, 1); r.add(1, 2); r.add(2, 3)
    r.touch(1, 2)  # make frame 1 most recent
    # pick victim should be 0
    victim, page = r.pick_victim()
    assert victim == 0

def test_clock_cycles():
    r = ClockReplacer(3)
    r.add(0, 1); r.add(1, 2); r.add(2, 3)
    # repeatedly pick to ensure it returns a victim without error
    v,p = r.pick_victim()
    assert isinstance(v, int)