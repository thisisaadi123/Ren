from ren_check import tree, integer, is_bst


def validate(root, x):
    tree("root", root, 10**4, 0, 10**9, distinct=True)
    assert is_bst(root), "the tree must be a valid binary search tree"
    integer("x", x, 0, 10**9)
