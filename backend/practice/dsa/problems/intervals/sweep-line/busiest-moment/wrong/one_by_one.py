class Solution:
    # Mistake: applies events one at a time even when several happen at the same minute.
    def busiestMoment(self, visits):
        ev = []
        for s, e in visits:
            ev.append((s, 1))
            ev.append((e + 1, -1))
        ev.sort(key=lambda x: (x[0], -x[1]))
        cur = best = 0
        at = None
        for t, d in ev:
            cur += d
            if cur > best:
                best, at = cur, t
        return at
