def validate(calls):
    assert isinstance(calls, list) and calls, "calls is a non-empty list"
    assert calls[0] == ["PriceStreak"], "the first call creates the tracker"
    assert len(calls) - 1 <= 10**5, "at most 10^5 calls to record"
    for c in calls[1:]:
        assert c[0] == "record" and len(c) == 2, "only record(price) calls follow"
        assert type(c[1]) is int and 1 <= c[1] <= 10**9, "1 <= price <= 10^9"
