from ren_check import integer
def validate(n, groups):
    integer("n", n, 1, 100_000)
    assert isinstance(groups, list) and 1 <= len(groups) <= 100_000, "1 to 10^5 groups"
    for g in groups:
        assert isinstance(g, list) and len(g) == 3, "each group is [l, r, people]"
        l, r, p = g
        assert type(l) is int and type(r) is int and 0 <= l <= r < n, "0 <= l <= r < n"
        assert type(p) is int and 1 <= p <= 10**4, "1 <= people <= 10^4"
