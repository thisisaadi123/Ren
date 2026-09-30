from ren_check import tree


def validate(root):
    tree("root", root, 10**4, -2**31, 2**31 - 1, min_nodes=1)
