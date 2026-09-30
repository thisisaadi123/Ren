from ren_check import ints
def validate(scores, queries):
    ints("scores", scores, 1, 100_000, -10**9, 10**9)
    assert isinstance(queries, list) and 1 <= len(queries) <= 100_000, "1 to 10^5 queries"
    for q in queries:
        assert isinstance(q, list) and len(q) == 2, "each query is [lo, hi]"
        assert type(q[0]) is int and type(q[1]) is int and -10**9 <= q[0] <= q[1] <= 10**9, "-10^9 <= lo <= hi <= 10^9"
