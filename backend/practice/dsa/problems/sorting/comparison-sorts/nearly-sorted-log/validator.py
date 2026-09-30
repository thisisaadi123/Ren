from ren_check import ints, integer
def validate(times, k):
    ints("times", times, 1, 100_000, 0, 10**9)
    integer("k", k, 0, 10)
    order = sorted(range(len(times)), key=lambda i: (times[i], i))
    # Some sorted arrangement must place every entry within k of where it is.
    s = sorted(times)
    for i, t in enumerate(times):
        lo, hi = max(0, i - k), min(len(times), i + k + 1)
        assert t in s[lo:hi], "every entry must be at most k positions from its sorted position"
