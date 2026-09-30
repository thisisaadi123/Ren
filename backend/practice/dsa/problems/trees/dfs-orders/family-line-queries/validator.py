from ren_check import tree


def validate(root, queries):
    values = tree("root", root, 10**5, 1, 10**6, min_nodes=1, distinct=True)
    assert isinstance(queries, list) and 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    have = set(values)
    for q in queries:
        assert isinstance(q, list) and len(q) == 2, "each query is [a, b]"
        assert q[0] in have and q[1] in have, "both IDs of every query are in the tree"
