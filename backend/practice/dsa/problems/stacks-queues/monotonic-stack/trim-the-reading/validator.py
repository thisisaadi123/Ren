from ren_check import text, integer
def validate(num, k):
    text("num", num, 1, 10**5, "0123456789")
    assert num == "0" or num[0] != "0", "num has no leading zeros"
    integer("k", k, 1, len(num))
