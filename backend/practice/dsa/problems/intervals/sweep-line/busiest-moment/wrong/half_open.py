class Solution:
    # Mistake: treats the leave minute as already gone.
    def busiestMoment(self, visits):
        from collections import Counter
        ev = Counter()
        for s, e in visits:
            ev[s] += 1
            ev[e] -= 1
        cur = best = 0
        at = visits[0][0]
        for t in sorted(ev):
            cur += ev[t]
            if cur > best:
                best, at = cur, t
        return at
