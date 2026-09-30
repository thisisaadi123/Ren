from ren_check import ints
def validate(labels):
    n = len(labels)
    ints("labels", labels, 2, 100_000, 1, n)
    assert len(set(labels)) == n - 1, "exactly one number must appear twice"
