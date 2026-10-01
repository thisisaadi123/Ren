def validate(a, b):
    for s in (a, b):
        assert type(s) is str and 1 <= len(s) <= 100_000, "1 <= length <= 10^5"
        assert all("a" <= c <= "z" or c == "#" for c in s), "lowercase letters and # only"
