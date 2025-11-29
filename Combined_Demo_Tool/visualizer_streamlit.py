"""
Minimal Streamlit visualizer: shows last N events from events.log and a simple count table.

Run with:
streamlit run Combined_Demo_Tool/visualizer_streamlit.py
"""

import streamlit as st
import json
import os
from collections import Counter

EVENTS_LOG = os.path.join(os.getcwd(), "events.log")

st.title("Virtual Memory Events Visualizer (minimal)")
st.markdown("Shows last 50 events and a simple event-type count summary.")

def load_events(n=50):
    if not os.path.exists(EVENTS_LOG):
        return []
    with open(EVENTS_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()
    events = [json.loads(l) for l in lines]
    return events[-n:]

events = load_events(200)
if not events:
    st.info("No events.log found. Run demo first.")
else:
    st.write("Last events (most recent first):")
    for ev in reversed(events[-50:]):
        st.json(ev)
    counts = Counter([e.get("type") for e in events])
    st.write("Event counts:")
    st.table(dict(counts))
