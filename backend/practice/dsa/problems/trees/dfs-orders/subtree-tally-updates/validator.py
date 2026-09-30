from ren_check import tree


def validate(root, ops):
    values = tree("root", root, 10**5, 1, 10**6, min_nodes=1, distinct=True)
    have = set(values)
    assert isinstance(ops, list) and 1 <= len(ops) <= 10**5, "1 <= ops.length <= 10^5"
    for op in ops:
        assert isinstance(op, list) and op and op[0] in (1, 2), "each op starts with 1 or 2"
        if op[0] == 1:
            assert len(op) == 3, "an add is [1, v, x]"
            assert type(op[2]) is int and 1 <= op[2] <= 10**9, "1 <= x <= 10^9"
        else:
            assert len(op) == 2, "a report is [2, v]"
        assert op[1] in have, "v is always in the tree"
