def validate(calls):
    assert isinstance(calls, list) and calls and calls[0] == ["PrefixTree"], "the first call creates the tree"
    assert len(calls) <= 30_001, "at most 3 * 10^4 calls"
    for c in calls[1:]:
        assert c[0] in ("insert", "search", "startsWith") and len(c) == 2, "unknown call"
        s = c[1]
        assert type(s) is str and 1 <= len(s) <= 50 and all("a" <= ch <= "z" for ch in s), "1 <= length <= 50, lowercase"
