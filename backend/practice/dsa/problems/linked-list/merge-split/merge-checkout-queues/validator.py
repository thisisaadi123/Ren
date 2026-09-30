def validate(queues):
    assert isinstance(queues, list), "queues is a list of lists"
    assert len(queues) <= 10_000, "at most 10^4 queues"
    total = 0
    for q in queues:
        assert isinstance(q, list), "each queue is given as a list of values"
        assert all(type(v) is int and -10**4 <= v <= 10**4 for v in q), "-10^4 <= node value <= 10^4"
        assert all(q[i] <= q[i + 1] for i in range(len(q) - 1)), "each queue is in non-decreasing order"
        total += len(q)
    assert total <= 100_000, "at most 10^5 nodes in total"
