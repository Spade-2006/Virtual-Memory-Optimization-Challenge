📘 Virtual Memory Optimization Tool

A complete simulator for Paging, Segmentation, Page Faults & Demand Paging

📌 Overview

This project is an interactive virtual memory management simulator designed to demonstrate how operating systems handle memory internally. It visually explains concepts such as paging, segmentation, address translation, page faults, demand paging, and page replacement algorithms.
The goal is to help students and educators understand complex OS memory mechanisms through clear animations, step-by-step execution, and real-time memory inspection.

🚀 Features
🔹 Paging Simulation
Virtual → Physical address translation
Page tables with valid, dirty, and referenced bits
Demand paging support
Real-time detection of page faults
🔹 Segmentation Support
Segment table visualization
Base–limit checks
Segmentation fault handling
Optional segmented + paged mode

🔹 Page Replacement Algorithms
FIFO
LRU
Optimal
Clock (Second Chance)
Frame visualization during eviction
Page fault comparison charts

🔹 Interactive GUI
Visualization of physical memory frames
Page table and segment table viewer
Step-by-step trace execution
Auto-play mode with adjustable speed
Color-coded process pages
Event logs showing faults, loads & evictions

🔹 Analytics Dashboard
Page fault graphs
Comparison of algorithms
TLB hit/miss charts
Exportable CSV/PNG reports

🧩 System Architecture
/simulation_core     → Paging, Segmentation, TLB, Algorithms
/gui_frontend        → User Interface & Visualization
/analytics           → Graphs, metrics, comparisons
/traces              → Sample memory access traces
/docs                → Documentation, diagrams

📥 Installation
Backend
pip install -r requirements.txt
python main.py

Frontend
npm install
npm start

▶️ Usage

Launch backend & frontend.
Load a sample trace or create your own.
Select frame size, algorithm, and mode (paging / segmentation).
Step through execution or enable auto-play.
Observe memory layout, faults, and TLB behavior live.
View analytics and export results.


🎯 Purpose

This tool is created for Operating Systems lab demonstrations, college projects, and self-learning. It provides an intuitive and visual understanding of virtual memory, making it easier to grasp how modern OSes manage memory.

📎 Future Improvements

Memory compaction visualization
Process scheduling integration
ML-driven page prefetching
Dark/light themes

🙌 Acknowledgements

Developed as part of an OS project to explore and visualize virtual memory concepts.