def validate(root):
    assert isinstance(root, list), "root is given in level order"
    values = [v for v in root if v is not None]
    assert len(values) <= 10_000, "at most 10^4 nodes"
    assert all(type(v) is int and -1000 <= v <= 1000 for v in values), "-1000 <= value <= 1000"
    assert not root or root[0] is not None, "an empty tree is []"
    assert not root or root[-1] is not None, "level order has no trailing nulls"
    # Every non-null entry after the root must have a parent: count open child slots.
    slots = 1
    for v in root:
        assert slots > 0, "a value has no parent"
        slots -= 1
        if v is not None:
            slots += 2
