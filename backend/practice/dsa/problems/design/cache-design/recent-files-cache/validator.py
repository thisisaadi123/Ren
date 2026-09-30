def validate(calls):
    assert isinstance(calls, list) and calls, "calls is a non-empty list"
    first = calls[0]
    assert first[0] == "RecentFilesCache" and len(first) == 2, "the first call creates the cache"
    assert type(first[1]) is int and 1 <= first[1] <= 3000, "1 <= capacity <= 3000"
    assert len(calls) - 1 <= 200_000, "at most 2 * 10^5 calls"
    for call in calls[1:]:
        name = call[0]
        assert name in ("open", "save"), "unknown method %r" % name
        assert type(call[1]) is int and 0 <= call[1] <= 10_000, "0 <= fileId <= 10^4"
        if name == "open":
            assert len(call) == 2, "open takes one argument"
        else:
            assert len(call) == 3 and type(call[2]) is int and 0 <= call[2] <= 100_000, "0 <= size <= 10^5"
