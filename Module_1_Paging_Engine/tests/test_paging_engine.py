import pytest
from Module_1_Paging_Engine.paging_engine import PagingEngine

def test_basic_load_and_reuse(tmp_path, monkeypatch):
    # create isolated tick file and events.log in tmp_path
    monkeypatch.chdir(tmp_path)
    pe = PagingEngine(frames_count=2, page_size=4096, policy="FIFO")
    # load page 1
    r1 = pe.handle_page_load_request(pid=1, gpage=1, access_type="R")
    assert r1["status"] == "loaded"
    f1 = r1["frame"]
    assert isinstance(f1, int)
    # load page 1 again -> ok
    r2 = pe.handle_page_load_request(pid=1, gpage=1, access_type="R")
    assert r2["status"] == "ok"
    assert r2["frame"] == f1

def test_eviction_and_dirty_writeback(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pe = PagingEngine(frames_count=1, page_size=4096, policy="FIFO")
    # load page 10, write to it (dirty)
    pe.handle_page_load_request(pid=2, gpage=10, access_type="W")
    # load page 20 -> should evict 10 and produce new frame
    r = pe.handle_page_load_request(pid=2, gpage=20, access_type="R")
    assert r["status"] == "loaded"
    assert pe.is_present(20)
    assert not pe.is_present(10)