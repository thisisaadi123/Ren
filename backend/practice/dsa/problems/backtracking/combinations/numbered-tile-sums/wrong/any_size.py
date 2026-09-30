class Solution:
    # Mistake: records a set as soon as the total matches, whatever its size.
    def tileSums(self, m, k, target):
        out, cur = [], []
        def go(nxt, left):
            if left == 0:
                if len(cur) <= k:
                    out.append(cur[:])
                return
            for t in range(nxt, m + 1):
                if t > left:
                    break
                cur.append(t)
                go(t + 1, left - t)
                cur.pop()
        go(1, target)
        return out
