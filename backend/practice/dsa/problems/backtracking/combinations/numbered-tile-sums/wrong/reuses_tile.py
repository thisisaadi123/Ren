class Solution:
    # Mistake: recurses from t instead of t + 1, so a tile can be drawn twice.
    def tileSums(self, m, k, target):
        out, cur = [], []
        def go(nxt, need, left):
            if need == 0:
                if left == 0:
                    out.append(cur[:])
                return
            for t in range(nxt, m + 1):
                if t > left:
                    break
                cur.append(t)
                go(t, need - 1, left - t)
                cur.pop()
        go(1, k, target)
        return out
