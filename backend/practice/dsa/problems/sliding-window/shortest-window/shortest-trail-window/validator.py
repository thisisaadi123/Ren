def validate(s, t):
    assert type(s) is str and 1 <= len(s) <= 20_000, "1 <= s.length <= 2 * 10^4"
    assert type(t) is str and 1 <= len(t) <= 100, "1 <= t.length <= 100"
    assert all("a" <= c <= "z" for c in s + t), "lowercase letters only"
