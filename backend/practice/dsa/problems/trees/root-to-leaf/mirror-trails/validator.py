from ren_check import tree


def validate(root):
    tree("root", root, 10**5, 1, 9, min_nodes=1)
