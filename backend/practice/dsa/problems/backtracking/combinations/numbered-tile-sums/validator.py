from ren_check import integer
def validate(m, k, target):
    integer("m", m, 1, 20)
    integer("k", k, 1, m)
    integer("target", target, 1, 210)
