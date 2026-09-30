from ren_check import tree, integer


def validate(root, target):
    tree("root", root, 3000, -1000, 1000)
    integer("target", target, -10**7, 10**7)
