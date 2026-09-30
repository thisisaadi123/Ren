from ren_check import tree, is_bst, integer


def validate(root, target):
    tree("root", root, 10**5, -10**9, 10**9, min_nodes=1, distinct=True)
    assert is_bst(root), "the tree must be a valid binary search tree"
    integer("target", target, -2 * 10**9, 2 * 10**9)
