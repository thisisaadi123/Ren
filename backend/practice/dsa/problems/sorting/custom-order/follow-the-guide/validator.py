from ren_check import ints
def validate(items, guide):
    ints("items", items, 1, 100_000, 0, 10**9)
    ints("guide", guide, 1, 100_000, 0, 10**9)
    assert len(set(guide)) == len(guide), "guide values must be distinct"
