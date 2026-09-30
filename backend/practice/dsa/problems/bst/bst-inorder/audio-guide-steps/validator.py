from ren_check import tree, is_bst


def validate(root, ops):
    vals = tree("root", root, 10**5, -10**9, 10**9, min_nodes=1, distinct=True)
    assert is_bst(root), "the tree must be a valid binary search tree"
    assert isinstance(ops, list) and 1 <= len(ops) <= 2 * 10**5, "1 <= ops.length <= 2 * 10^5"
    assert all(op in ("next", "hasNext") for op in ops), 'each op is "next" or "hasNext"'
    assert sum(op == "next" for op in ops) <= len(vals), '"next" is only used while an exhibit remains'
