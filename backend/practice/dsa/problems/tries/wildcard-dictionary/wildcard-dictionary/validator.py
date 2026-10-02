def validate(calls):
    assert isinstance(calls, list) and calls and calls[0] == ["WildcardDictionary"], "the first call creates the dictionary"
    assert len(calls) <= 10_001, "at most 10^4 calls"
    for c in calls[1:]:
        assert c[0] in ("addWord", "search") and len(c) == 2, "unknown call"
        s = c[1]
        assert type(s) is str and 1 <= len(s) <= 25, "1 <= length <= 25"
        if c[0] == "addWord":
            assert all("a" <= ch <= "z" for ch in s), "words are lowercase"
        else:
            assert all("a" <= ch <= "z" or ch == "." for ch in s) and s.count(".") <= 3, "lowercase and at most 3 dots"
