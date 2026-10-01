def validate(s):
    assert type(s) is str and 3 <= len(s) <= 100_000, "3 <= s.length <= 10^5"
    assert all(c in "abc" for c in s), "only a, b and c"
