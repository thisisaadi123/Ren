class Solution:
    # Mistake: recurses from m instead of m + 1, so a member can sit on the committee twice.
    def committeePicks(self, n, k):
        out, cur = [], []
        def go(nxt):
            if len(cur) == k:
                out.append(cur[:])
                return
            for m in range(nxt, n + 1):
                cur.append(m)
                go(m)
                cur.pop()
        go(1)
        return out
