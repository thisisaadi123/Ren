def validate(calls):
    assert isinstance(calls, list) and calls, "calls is a non-empty list"
    c0 = calls[0]
    assert c0[0] == "RingBuffer" and len(c0) == 2 and type(c0[1]) is int and 1 <= c0[1] <= 1000, "RingBuffer(k) with 1 <= k <= 1000"
    assert len(calls) <= 100_001, "at most 10^5 calls"
    for c in calls[1:]:
        if c[0] == "enqueue":
            assert len(c) == 2 and type(c[1]) is int and 0 <= c[1] <= 1000, "0 <= x <= 1000"
        else:
            assert len(c) == 1 and c[0] in ("dequeue", "front", "rear", "isEmpty", "isFull"), "unknown call"
