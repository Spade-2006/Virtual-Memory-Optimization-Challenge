# 📘 Virtual Memory Optimization Challenge

### A complete simulator for Paging, Segmentation, Page Faults & Demand Paging (CLI-based + Analytics)

## 📌 Overview

This project is a deterministic, test-driven virtual memory simulator built for Operating Systems labs and academic demonstrations. It models how an OS handles Paging, Segmentation, Segmented-Paging, Page Faults, and Demand Paging. It includes Page Replacement Algorithms (FIFO, LRU, Optimal, Clock). All memory operations generate structured JSON events in `events.log`, allowing students and instructors to replay, visualize, and analyze OS memory behavior step-by-step.

**The repository includes:**

  * A complete paging engine
  * A segmentation engine with allocator
  * A global page registry
  * A demand paging controller
  * Offline analytics (FIFO vs LRU vs Optimal)
  * CLI demo runner
  * Minimal Streamlit visualizer

## 🚀 Features

**🔹 Paging Simulation**

  * Virtual → physical page translation
  * Page Table Entries: present, dirty, referenced, frame
  * Deterministic page faults
  * Demand paging
  * Replacement algorithms: FIFO / LRU / CLOCK

**🔹 Segmentation**

  * Base–limit checks
  * Segment allocation: First Fit / Best Fit / Worst Fit
  * Segmentation faults
  * Segmented + Paging mode
  * Global page ID mapping per (pid, segment, page)

**🔹 Demand Paging Controller**

  * Simulated disk latency
  * Prevents duplicate page loads
  * Handles: `page_load_request`, `page_in`, `page_out`
  * Tight integration with PagingEngine

**🔹 Event Logging (JSON-lines)**
Every major step logs a structured event to `events.log` (e.g., `page_fault`, `page_in`, `page_out`, `segment_alloc`, `tlb_hit`, `access_request`). These logs let students inspect memory evolution frame-by-frame.

**🔹 Analytics Dashboard (CLI)**
Located in `Combined_Demo_Tool/analytics.py`:

  * Offline page fault comparison: FIFO vs LRU vs Optimal
  * Exports results to `analytics.csv`
  * Pre-built sample traces: locality, sequential, mixed

**🔹 Minimal Streamlit Visualizer (Optional)**
Displays last N events and event count table. Run with: `streamlit run Combined_Demo_Tool/visualizer_streamlit.py`

## 🧩 System Architecture

```text
Virtual Memory Optimization Challenge/
│
├── Module_1_Paging_Engine
│   → Paging, frames, replacement algorithms, TLB
│
├── Module_2_Segmentation_DemandPaging
│   → Segmentation, allocator, registry, demand paging
│
├── Combined_Demo_Tool
│   → Demo runner, traces, analytics, visualizer
│
├── docs
│   → Reports, diagrams
│
└── events.log
    → Auto-generated at runtime
```

**Core Workflow:**
Trace CSV → SegmentationEngine translates segment offset → Virtual page ID generated → DemandController requests the page → PagingEngine loads/evicts frames → Event logged to `events.log`

## 📥 Installation

**Backend Setup**

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

**Run Demo**

```bash
python Combined_Demo_Tool/run_demo.py Combined_Demo_Tool/traces/locality.csv
```

**Run Analytics**

```bash
python Combined_Demo_Tool/analytics.py Combined_Demo_Tool/traces/locality.csv
```

**Run Visualizer (optional)**

```bash
streamlit run Combined_Demo_Tool/visualizer_streamlit.py
```

**Run Tests**

```bash
pytest -q
```

## ▶️ Usage

1.  Choose a sample trace (`locality.csv`, `sequential.csv`, `mixed_multi.csv`).
2.  Run `run_demo.py` with the trace path.
3.  The demo creates 32KB segments for each PID, translates segment offsets into global pages, uses demand paging, and employs LRU replacement by default.
4.  Inspect `events.log` to study: `page_fault`, `page_in`, `segment_alloc`, `tlb_hit`, `segmentation faults`.
5.  Run `analytics.py` to generate page fault charts.

## 🎯 Purpose

This tool is ideal for:

  * OS labs and academic projects
  * Teaching paging, segmentation, and demand paging
  * Understanding real OS memory management
  * Research with frame counts & replacement algorithms
    It prioritizes clarity, determinism, and educational insight.

## 📎 Future Improvements

  * Memory compaction visualization
  * Multi-process scheduling integration
  * TLB replacement strategies
  * Full GUI (Tkinter / React)
  * Dark/light theme for visualizer
  * Exportable event replay animation

## 🙌 Acknowledgements

Developed as part of an Operating Systems project exploring virtual memory, with emphasis on deterministic testing, event-driven architecture, and educational clarity.