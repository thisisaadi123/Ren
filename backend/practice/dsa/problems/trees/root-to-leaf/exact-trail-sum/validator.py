from ren_check import tree, integer


def validate(root, target):
    tree("root", root, 10**5, -1000, 1000)
    integer("target", target, -10**8, 10**8)
