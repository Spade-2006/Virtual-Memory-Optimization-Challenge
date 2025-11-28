📘 Virtual Memory Optimization Challenge
A complete simulator for Paging, Segmentation, Page Faults & Demand Paging (CLI-based + Analytics)
📌 Overview

This project is a fully deterministic, test-driven virtual memory simulator built for Operating Systems labs and academic demonstrations.
It models how an OS handles:

Paging

Segmentation

Segmented-Paging

Page faults

Demand paging

Page replacement algorithms (FIFO, LRU, Optimal, Clock)

All memory operations generate structured JSON events in events.log, allowing instructors and students to replay, visualize, and analyze internal OS behaviors step-by-step.

The repository includes:

A complete paging engine

A segmentation engine with allocator

A global page registry

A demand paging controller

Offline analytics (FIFO vs LRU vs Optimal)

CLI demo runner

Minimal Streamlit visualizer

Sample traces

🚀 Features
🔹 Paging Simulation

Virtual → physical page translation

Page Table Entries: present, dirty, referenced, frame

Deterministic page faults

Demand paging support

FIFO / LRU / CLOCK replacement

🔹 Segmentation

Base–limit checks

Segment allocation via: First Fit / Best Fit / Worst Fit

Segmentation faults

Segmented + Paging mode

Global page ID mapping per (pid, segment, page)

🔹 Demand Paging Controller

Simulated disk latency

Prevents duplicate page loads

Handles page_load_request, page_in, page_out

Integrates tightly with PagingEngine

🔹 Event Logging (JSON-lines)

Every major step logs a structured event to events.log:

page_fault, page_in, page_out,
segment_alloc, seg_translate,
tlb_hit, tlb_miss,
access_request, demand_page_loaded, analytics_summary


This lets students inspect memory evolution frame-by-frame.

🔹 Analytics Dashboard (CLI)

Located in Combined_Demo_Tool/analytics.py

Offline page fault comparison: FIFO vs LRU vs Optimal

Exports results to analytics.csv

Pre-built sample traces (locality, sequential, mixed)

🔹 Minimal Streamlit Visualizer (Optional)

Shows:

Last N events in real time

Simple event count table
Run with:

streamlit run Combined_Demo_Tool/visualizer_streamlit.py

🧩 System Architecture
Virtual Memory Optimization Challenge/
│
├── Module_1_Paging_Engine        → Paging, frames, replacement algorithms, TLB
├── Module_2_Segmentation_DemandPaging → Segmentation, allocator, registry, demand paging
├── Combined_Demo_Tool            → Demo runner, traces, analytics, visualizer
├── docs                          → Reports, diagrams (your project docs)
└── events.log                    → Auto-generated at runtime


Core workflow:

Trace CSV
→ SegmentationEngine translates segment offset
→ virtual page ID produced
→ DemandController requests the page
→ PagingEngine loads/evicts pages
→ events logged to events.log

📥 Installation
Backend
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

Run Demo
python Combined_Demo_Tool/run_demo.py Combined_Demo_Tool/traces/locality.csv

Run Analytics
python Combined_Demo_Tool/analytics.py Combined_Demo_Tool/traces/locality.csv

Visualizer (optional)
streamlit run Combined_Demo_Tool/visualizer_streamlit.py

Run Tests
pytest -q

▶️ Usage

Choose a sample trace (locality.csv, sequential.csv, mixed_multi.csv).

Run run_demo.py with the trace path.

The demo:

Creates 32KB segments for each PID

Translates segment offsets into global pages

Requests pages using demand paging

Uses LRU replacement by default

Inspect events.log to see:

page_faults

page_in/page_out

segment_alloc

tlb_hit/tlb_miss

segmentation faults

Run analytics.py for page fault charts.

🎯 Purpose

This tool is ideal for:

Operating Systems labs

College minor/major projects

Teaching paging, segmentation, and demand paging

Understanding real OS memory management

Research experiments with frame counts & algorithms

The simulator focuses on clarity, determinism, and insight, making complex OS internals easier to understand.

📎 Future Improvements

Memory compaction visualization

Multi-process scheduling integration

TLB replacement algorithms

Full GUI (Tkinter / React) extension

Dark/light theme in visualizer

Exportable event replay animation

🙌 Acknowledgements

Developed as part of an Operating Systems project exploring virtual memory.
Special focus on deterministic testing, event-driven architecture, and educational clarity.