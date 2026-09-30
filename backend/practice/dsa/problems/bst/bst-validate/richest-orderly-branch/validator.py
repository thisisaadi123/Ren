from ren_check import tree


def validate(root):
    tree("root", root, 4 * 10**4, -4 * 10**4, 4 * 10**4, min_nodes=1)
