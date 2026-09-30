class Solution:
    def committeePicks(self, n, k):
        out, cur = [], []

        def go(nxt):
            if len(cur) == k:
                out.append(cur[:])
                return
            need = k - len(cur)
            for m in range(nxt, n - need + 2):
                cur.append(m)
                go(m + 1)
                cur.pop()

        go(1)
        return out
