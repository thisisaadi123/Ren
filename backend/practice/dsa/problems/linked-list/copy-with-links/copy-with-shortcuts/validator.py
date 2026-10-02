def validate(head):
    assert isinstance(head, list) and len(head) <= 100_000, "0 <= n <= 10^5"
    for p in head:
        assert isinstance(p, list) and len(p) == 2, "each clue is [val, random]"
        assert type(p[0]) is int and -10**4 <= p[0] <= 10**4, "-10^4 <= val <= 10^4"
        assert p[1] is None or (type(p[1]) is int and 0 <= p[1] < len(head)), "random is null or a clue's index"
