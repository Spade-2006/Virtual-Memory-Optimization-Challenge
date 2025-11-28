# """
# DemandController ties segmentation-level requests to the PagingEngine.
# It avoids duplicate concurrent page loads by tracking pending requests.
# A small sleep simulates disk latency; default 0.02s (deterministic in tests can be set to 0).
# """

# import time
# from typing import Dict, Set
# #from Module_1_Paging_Engine.paging_engine import PagingEngine
# from . import events as ev

# class DemandController:
#     def __init__(self, paging_engine: PagingEngine, disk_latency_s: float = 0.02):
#         self.paging_engine = paging_engine
#         self.disk_latency_s = disk_latency_s
#         # presence cache: (pid, global_page) -> True
#         self.presence: Dict[tuple, bool] = {}
#         self.pending: Set[tuple] = set()

#     def request_page(self, pid: int, global_page: int, access_type: str = "R"):
#         key = (pid, global_page)
#         ev.emit_page_load_request(pid, global_page, reason="demand")
#         # if presence known and present, return
#         if self.paging_engine.is_present(global_page):
#             return {"status": "ok", "frame": self.paging_engine.ptes[global_page].frame}
#         # avoid duplicate loads
#         if key in self.pending:
#             # simple busy-wait for deterministic small number of loops (no background threads)
#             loops = 0
#             while key in self.pending and loops < 1000:
#                 loops += 1
#             if self.paging_engine.is_present(global_page):
#                 return {"status": "ok", "frame": self.paging_engine.ptes[global_page].frame}
#         # mark pending
#         self.pending.add(key)
#         # simulate latency
#         if self.disk_latency_s > 0:
#             time.sleep(self.disk_latency_s)
#         result = self.paging_engine.handle_page_load_request(pid, global_page, access_type=access_type)
#         # mark loaded
#         frame = result.get("frame")
#         ev.emit_demand_page_loaded(pid, global_page, frame)
#         self.presence[key] = True
#         self.pending.discard(key)
#         return {"status": "loaded", "frame": frame}
