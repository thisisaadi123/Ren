from ren_check import tree


def validate(root):
    tree("root", root, 10**5, -1000, 1000)
    assert None not in root, "the tree must be complete"
