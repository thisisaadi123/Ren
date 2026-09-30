class Solution:
    # Mistake: stores the working list itself instead of a copy; after backtracking every stored entry is empty.
    def committeePicks(self, n, k):
        out, cur = [], []
        def go(nxt):
            if len(cur) == k:
                out.append(cur)
                return
            for m in range(nxt, n + 1):
                cur.append(m)
                go(m + 1)
                cur.pop()
        go(1)
        return out
