from ren_check import tree


def validate(root):
    tree("root", root, 10**4, 0, 25, min_nodes=1)
