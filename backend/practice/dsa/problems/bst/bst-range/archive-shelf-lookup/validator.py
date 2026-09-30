from ren_check import tree, is_bst


def validate(root, queries):
    tree("root", root, 10**5, 0, 10**9, min_nodes=1, distinct=True)
    assert is_bst(root), "the tree must be a valid binary search tree"
    assert isinstance(queries, list) and 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    for q in queries:
        assert isinstance(q, list) and len(q) == 3 and all(type(x) is int for x in q), "each query is [low, high, k]"
        low, high, k = q
        assert 0 <= low <= high <= 10**9, "0 <= low <= high <= 10^9"
        assert 1 <= k <= 10**5, "1 <= k <= 10^5"
