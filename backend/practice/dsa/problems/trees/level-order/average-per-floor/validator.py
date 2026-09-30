from ren_check import tree


def validate(root):
    tree("root", root, 10**5, -10**9, 10**9, min_nodes=1)
