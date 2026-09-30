import string
from ren_check import text
def validate(a, b):
    for name, s in (("a", a), ("b", b)):
        text(name, s, 1, 10**5, string.ascii_letters + " ")
        assert s.strip(" "), "%s has at least one letter" % name
