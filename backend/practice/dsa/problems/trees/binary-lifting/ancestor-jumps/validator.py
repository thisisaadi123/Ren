def validate(parent, queries):
    n = len(parent)
    assert isinstance(parent, list) and 1 <= n <= 50_000, "1 <= n <= 5 * 10^4"
    assert parent[0] == -1, "parent[0] = -1"
    assert all(type(p) is int and 0 <= p < n and p != i for i, p in enumerate(parent) if i), "parents are people 0..n-1"
    # Every node must reach 0 without a cycle.
    state = [0] * n
    state[0] = 2
    for s in range(n):
        path, v = [], s
        while state[v] == 0:
            state[v] = 1
            path.append(v)
            v = parent[v]
        assert state[v] == 2, "the parent links contain a cycle"
        for x in path:
            state[x] = 2
    assert isinstance(queries, list) and 1 <= len(queries) <= 50_000, "1 <= queries.length <= 5 * 10^4"
    assert all(isinstance(q, list) and len(q) == 2 and type(q[0]) is int and type(q[1]) is int and 0 <= q[0] < n and 1 <= q[1] <= n for q in queries), "0 <= v < n, 1 <= k <= n"
