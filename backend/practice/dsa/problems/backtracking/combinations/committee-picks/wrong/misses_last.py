class Solution:
    # Mistake: loops over range(nxt, n), so member n is never picked.
    def committeePicks(self, n, k):
        out, cur = [], []
        def go(nxt):
            if len(cur) == k:
                out.append(cur[:])
                return
            for m in range(nxt, n):
                cur.append(m)
                go(m + 1)
                cur.pop()
        go(1)
        return out
