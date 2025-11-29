#!/usr/bin/env bash
python -u Combined_Demo_Tool/run_demo.py Combined_Demo_Tool/traces/locality.csv
python -u Combined_Demo_Tool/analytics.py
echo "Done"
