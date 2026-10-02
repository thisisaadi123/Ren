def validate(calls):
    assert isinstance(calls, list) and calls and calls[0] == ["TwoStackQueue"], "the first call creates the queue"
    assert len(calls) <= 100_001, "at most 10^5 calls"
    size = 0
    for c in calls[1:]:
        name = c[0]
        if name == "push":
            assert len(c) == 2 and type(c[1]) is int and 1 <= c[1] <= 10**9, "1 <= x <= 10^9"
            size += 1
        elif name in ("pop", "peek"):
            assert len(c) == 1 and size > 0, "pop and peek only on a non-empty queue"
            size -= name == "pop"
        else:
            assert c == ["empty"], "unknown call"
