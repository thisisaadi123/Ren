def validate(people):
    assert isinstance(people, list) and 1 <= len(people) <= 2000, "people must have 1 to 2000 pairs"
    for p in people:
        assert isinstance(p, list) and len(p) == 2, "each person is [height, ahead]"
        assert type(p[0]) is int and 1 <= p[0] <= 10**6, "height must be between 1 and 10^6"
        assert type(p[1]) is int and 0 <= p[1] < len(people), "ahead must be between 0 and n - 1"
    line = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
        assert k <= len(line), "the pairs must describe a real line"
        line.insert(k, [h, k])
    for i, (h, k) in enumerate(line):
        assert sum(1 for q in line[:i] if q[0] >= h) == k, "the pairs must describe a real line"
