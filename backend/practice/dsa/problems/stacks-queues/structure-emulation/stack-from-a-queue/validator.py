def validate(calls):
    assert isinstance(calls, list) and calls and calls[0] == ["QueueStack"], "the first call creates the stack"
    assert len(calls) <= 3001, "at most 3000 calls"
    size = 0
    for c in calls[1:]:
        name = c[0]
        if name == "push":
            assert len(c) == 2 and type(c[1]) is int and 1 <= c[1] <= 10**9, "1 <= x <= 10^9"
            size += 1
        elif name in ("pop", "top"):
            assert len(c) == 1 and size > 0, "pop and top only on a non-empty stack"
            size -= name == "pop"
        else:
            assert c == ["empty"], "unknown call"
