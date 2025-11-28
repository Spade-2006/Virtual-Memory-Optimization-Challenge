from Module_1_Paging_Engine.paging_engine import PagingEngine
from Module_2_Segmentation_DemandPaging.demand_controller import DemandController
import pytest
import time

def test_request_page(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pe = PagingEngine(frames_count=2, page_size=4096, policy="LRU")
    dc = DemandController(pe, disk_latency_s=0)  # zero latency for test speed
    res = dc.request_page(pid=1, global_page=1, access_type="R")
    assert res["status"] in ("loaded", "ok")
    # requesting same page should return ok and not raise
    res2 = dc.request_page(pid=1, global_page=1, access_type="R")
    assert res2["status"] in ("loaded", "ok")
