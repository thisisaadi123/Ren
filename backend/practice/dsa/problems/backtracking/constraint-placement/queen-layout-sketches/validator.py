from ren_check import integer
def validate(n, fixed):
    integer("n", n, 1, 9)
    assert isinstance(fixed, list) and len(fixed) <= n, "at most n glued queens"
    seen = set()
    for q in fixed:
        assert isinstance(q, list) and len(q) == 2, "each glued queen is [r, c]"
        r, c = q
        assert type(r) is int and type(c) is int and 0 <= r < n and 0 <= c < n, "coordinates are between 0 and n - 1"
        assert (r, c) not in seen, "glued squares are distinct"
        seen.add((r, c))
