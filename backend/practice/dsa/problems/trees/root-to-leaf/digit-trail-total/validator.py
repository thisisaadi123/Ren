from ren_check import tree


def validate(root):
    tree("root", root, 10**5, 0, 9, min_nodes=1)
