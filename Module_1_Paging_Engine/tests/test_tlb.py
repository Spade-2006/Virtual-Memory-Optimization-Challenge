import pytest
from Module_1_Paging_Engine.tlb import TLB
from Module_1_Paging_Engine.utils import emit_event, tick
import os, json

def test_tlb_insert_lookup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tlb = TLB(size=2)
    # initial miss
    assert tlb.lookup(pid=1, gpage=5) is None
    tlb.insert(pid=1, gpage=5, frame=0)
    assert tlb.lookup(pid=1, gpage=5) == 0
    tlb.insert(pid=1, gpage=6, frame=1)
    # insert third to evict LRU (5)
    tlb.insert(pid=1, gpage=7, frame=2)
    assert tlb.lookup(pid=1, gpage=5) is None