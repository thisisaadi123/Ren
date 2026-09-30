from ren_check import tree, is_bst, integer


def validate(root, low, high):
    tree("root", root, 10**4, 0, 10**4, min_nodes=1, distinct=True)
    assert is_bst(root), "the tree must be a valid binary search tree"
    integer("low", low, 0, 10**4)
    integer("high", high, low, 10**4)
