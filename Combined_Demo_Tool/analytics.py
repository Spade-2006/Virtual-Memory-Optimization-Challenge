"""
Analytics tools:
- build_global_trace: map CSV trace addresses to global pages using SegmentationEngine
- sweep: run offline FIFO, LRU, Optimal simulations over frames_min..frames_max and write analytics.csv
"""

import csv
import sys
import pandas as pd
from Module_2_Segmentation_DemandPaging.segmentation_engine import SegmentationEngine
from Module_1_Paging_Engine.paging_engine import PagingEngine
import os

def build_global_trace(trace_csv: str):
    se = SegmentationEngine(address_space_size=1<<20, allocator_algo="first_fit")
    gtrace = []
    # pre-scan pids to create segments
    pids = set()
    rows = []
    with open(trace_csv, newline='') as csvfile:
        r = csv.DictReader(csvfile)
        for row in r:
            row["pid"] = int(row["pid"])
            row["segment"] = int(row["segment"])
            row["segment_offset"] = int(row["segment_offset"])
            rows.append(row)
            pids.add(row["pid"])
    for pid in sorted(pids):
        se.create_segment(pid, seg_id=0, size_bytes=32*1024)
    for row in rows:
        trans = se.seg_translate(row["pid"], row["segment"], row["segment_offset"], mode="segmented-paging")
        gtrace.append(trans["virtual_page"])
    return gtrace

def sweep(trace_csv: str, frames_min=2, frames_max=8, out_csv="analytics.csv"):
    gtrace = build_global_trace(trace_csv)
    rows = []
    for frames in range(frames_min, frames_max+1):
        fifo_faults = PagingEngine.optimal_faults_for_trace(gtrace, frames_count=frames)  # here we reuse optimal function (intentionally)
        # For demonstration: compute optimal exactly, compute FIFO and LRU by running simple simulation via PagingEngine
        pe_fifo = PagingEngine(frames_count=frames, policy="FIFO")
        pe_lru = PagingEngine(frames_count=frames, policy="LRU")
        fifo_count = 0
        lru_count = 0
        for pg in gtrace:
            if not pe_fifo.is_present(pg):
                fifo_count += 1
                pe_fifo.handle_page_load_request(pid=0, gpage=pg)
            if not pe_lru.is_present(pg):
                lru_count += 1
                pe_lru.handle_page_load_request(pid=0, gpage=pg)
        optimal_count = PagingEngine.optimal_faults_for_trace(gtrace, frames)
        rows.append({"frames": frames, "fifo": fifo_count, "lru": lru_count, "optimal": optimal_count})
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv}")

if __name__ == "__main__":
    trace = "Combined_Demo_Tool/traces/locality.csv" if len(sys.argv) < 2 else sys.argv[1]
    sweep(trace)
