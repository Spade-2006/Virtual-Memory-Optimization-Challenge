from Module_2_Segmentation_DemandPaging.allocator import SimpleAllocator

def test_simple_alloc_free():
    a = SimpleAllocator(1024)
    b1 = a.first_fit(256)
    assert b1 == 0
    b2 = a.first_fit(256)
    assert b2 == 256
    assert a.free_block(b1)
    # after freeing base 0, first_fit should reuse it
    b3 = a.first_fit(128)
    assert b3 == 0

def test_best_worst_fit():
    a = SimpleAllocator(512)
    a.first_fit(100)  # base 0
    a.first_fit(100)  # base 100
    # free the first
    a.free_block(0)
    b = a.best_fit(50)
    assert b is not None
