def validate(s, t):
    assert type(s) is str and 1 <= len(s) <= 100_000, "1 <= s.length <= 10^5"
    assert type(t) is str and 1 <= len(t) <= 100_000, "1 <= t.length <= 10^5"
    assert all(c.isascii() and c.isalpha() for c in s + t), "English letters only"
