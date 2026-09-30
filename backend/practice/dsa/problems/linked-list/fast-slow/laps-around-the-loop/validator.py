def _nodes(head, max_n, lo, hi, min_n=0):
    if isinstance(head, dict):
        assert set(head) <= {"values", "cycle_at"} and "values" in head, "a looped list is {values, cycle_at}"
        values, at = head["values"], head.get("cycle_at", -1)
    else:
        values, at = head, -1
    assert isinstance(values, list), "the list is given as its values"
    assert min_n <= len(values) <= max_n, "the list has %d to %d nodes" % (min_n, max_n)
    assert all(type(v) is int and lo <= v <= hi for v in values), "node values must be between %d and %d" % (lo, hi)
    assert type(at) is int and -1 <= at < len(values), "cycle_at is -1 or the index of a node"
    return values, at


def validate(head, steps):
    _nodes(head, 100_000, 0, 10**9, min_n=1)
    assert isinstance(steps, list) and 1 <= len(steps) <= 100_000, "1 <= steps.length <= 10^5"
    assert all(type(s) is int and 0 <= s <= 10**15 for s in steps), "0 <= steps[i] <= 10^15"
