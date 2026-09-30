from ren_check import text
import string
def validate(gates, current):
    text("gates", gates, 2, 10_000, string.ascii_lowercase)
    assert list(gates) == sorted(gates), "gates must be sorted"
    assert len(set(gates)) >= 2, "gates must contain at least two different letters"
    text("current", current, 1, 1, string.ascii_lowercase)
