def validate(calls):
    assert isinstance(calls, list) and calls, "calls is a non-empty list"
    first = calls[0]
    assert first[0] == "TaskHeap" and len(first) == 2 and isinstance(first[1], list), "the first call creates the heap"
    assert len(first[1]) <= 10**5 and all(type(v) is int and 0 <= v <= 10**9 for v in first[1]), "0 <= items[i] <= 10^9"
    assert len(calls) - 1 <= 10**5, "at most 10^5 calls"
    for c in calls[1:]:
        assert c[0] in ("push", "pop", "peek", "size"), "unknown method %r" % c[0]
        if c[0] == "push":
            assert len(c) == 2 and type(c[1]) is int and 0 <= c[1] <= 10**9, "0 <= x <= 10^9"
        else:
            assert len(c) == 1, "%s takes no arguments" % c[0]
