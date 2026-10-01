def validate(a, b):
    for name, lst in (("a", a), ("b", b)):
        assert isinstance(lst, list) and 1 <= len(lst) <= 100_000, "1 <= %s length <= 10^5" % name
        assert all(type(v) is int and 0 <= v <= 9 for v in lst), "0 <= node value <= 9"
        assert lst[0] != 0 or len(lst) == 1, "%s has no leading zeros" % name
