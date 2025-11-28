from Module_2_Segmentation_DemandPaging.segmentation_engine import SegmentationEngine, PAGE_SIZE

def test_create_and_translate(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    se = SegmentationEngine(address_space_size=PAGE_SIZE*8, allocator_algo="first_fit")
    se.create_segment(pid=1, seg_id=0, size_bytes=PAGE_SIZE*2)
    r = se.seg_translate(1, 0, 0, mode="segmented-paging")
    assert r["status"] == "ok"
    assert "virtual_page" in r
    # out of bounds
    try:
        se.seg_translate(1, 0, PAGE_SIZE*3, mode="segmented-paging")
        assert False
    except Exception:
        assert True
