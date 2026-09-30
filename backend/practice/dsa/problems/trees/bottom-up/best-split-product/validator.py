from ren_check import tree


def validate(root):
    tree("root", root, 10**5, 1, 10**4, min_nodes=2)
