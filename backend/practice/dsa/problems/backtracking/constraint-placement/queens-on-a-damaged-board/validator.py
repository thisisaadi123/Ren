from ren_check import integer
def validate(n, holes):
    integer("n", n, 1, 11)
    assert isinstance(holes, list) and len(holes) <= n * n, "at most n² holes"
    seen = set()
    for h in holes:
        assert isinstance(h, list) and len(h) == 2, "each hole is [r, c]"
        r, c = h
        assert type(r) is int and type(c) is int and 0 <= r < n and 0 <= c < n, "hole coordinates are between 0 and n - 1"
        assert (r, c) not in seen, "holes are distinct"
        seen.add((r, c))
