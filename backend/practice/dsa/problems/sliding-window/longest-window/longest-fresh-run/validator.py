def validate(s):
    assert type(s) is str and 1 <= len(s) <= 100_000, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" or "0" <= c <= "9" for c in s), "lowercase letters and digits only"
