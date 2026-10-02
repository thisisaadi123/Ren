def validate(s):
    assert type(s) is str and 1 <= len(s) <= 12 and all("a" <= c <= "z" for c in s), "1 <= s.length <= 12, lowercase"
