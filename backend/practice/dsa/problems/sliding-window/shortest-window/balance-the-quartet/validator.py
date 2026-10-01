def validate(s):
    assert type(s) is str and 4 <= len(s) <= 100_000, "4 <= s.length <= 10^5"
    assert len(s) % 4 == 0, "s.length is a multiple of 4"
    assert all(c in "SATB" for c in s), "only S, A, T and B"
