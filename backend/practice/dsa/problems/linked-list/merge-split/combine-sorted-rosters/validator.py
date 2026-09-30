def validate(first, second):
    for name, lst in (("first", first), ("second", second)):
        assert isinstance(lst, list), "%s is given as a list of values" % name
        assert len(lst) <= 50_000, "each list has at most 5 * 10^4 nodes"
        assert all(type(v) is int and -10**6 <= v <= 10**6 for v in lst), "-10^6 <= node value <= 10^6"
        assert all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1)), "%s is in non-decreasing order" % name
