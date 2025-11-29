"""
Demo runner:
- Reads CSV trace file with header: time,pid,mode,segment,segment_offset,access_type
- Instantiates SegmentationEngine, PagingEngine (LRU default), DemandController
- Pre-creates a default 32KB segment per pid discovered
- Emits access_request events, translates, and does demand paging where needed
- Emits analytics_summary at end
"""

import csv
import sys
from Module_2_Segmentation_DemandPaging.segmentation_engine import SegmentationEngine
from Module_1_Paging_Engine.paging_engine import PagingEngine
from Module_2_Segmentation_DemandPaging.demand_controller import DemandController
from Module_2_Segmentation_DemandPaging import events as seg_events
from Module_2_Segmentation_DemandPaging import utils as seg_utils
from Module_1_Paging_Engine import utils as m1_utils
import os

def run(trace_path: str):
    # clear events.log and tick file for deterministic run
    evt = os.path.join(os.getcwd(), "events.log")
    tickf = os.path.join(os.getcwd(), "vm_tick.json")
    for f in (evt, tickf):
        if os.path.exists(f):
            os.remove(f)

    # read trace to discover PIDs
    pids = set()
    rows = []
    with open(trace_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader:
            r["pid"] = int(r["pid"])
            r["segment"] = int(r["segment"])
            r["segment_offset"] = int(r["segment_offset"])
            rows.append(r)
            pids.add(r["pid"])

    # instantiate engines
    seg_engine = SegmentationEngine(address_space_size=1<<20, allocator_algo="first_fit")
    paging = PagingEngine(frames_count=4, page_size=4096, policy="LRU")
    dc = DemandController(paging, disk_latency_s=0.01)

    # pre-create default 32KB segment per pid (seg_id 0)
    for pid in sorted(pids):
        seg_engine.create_segment(pid, seg_id=0, size_bytes=32*1024)

    total_accesses = 0
    total_page_faults = 0

    for r in rows:
        total_accesses += 1
        seg_events.emit_access_request(r["pid"], r["mode"], r["segment"], r["segment_offset"], r["access_type"])
        trans = seg_engine.seg_translate(r["pid"], r["segment"], r["segment_offset"], mode="segmented-paging")
        # request page via demand controller
        gpage = trans["virtual_page"]
        res = dc.request_page(r["pid"], gpage, access_type=r["access_type"])
        if res["status"] == "loaded":
            total_page_faults += 1

    # emit analytics summary
    summary = {
        "type": "analytics_summary",
        "total_accesses": total_accesses,
        "total_page_faults": total_page_faults,
        "frames": paging.frames_count
    }
    m1_utils.emit_event(summary)
    print("Demo complete. Events written to events.log")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Combined_Demo_Tool/run_demo.py <trace.csv>")
        sys.exit(1)
    run(sys.argv[1])
