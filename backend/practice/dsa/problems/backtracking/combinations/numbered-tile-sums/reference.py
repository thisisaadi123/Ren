class Solution:
    def tileSums(self, m, k, target):
        out, cur = [], []

        def go(nxt, need, left):
            if need == 0:
                if left == 0:
                    out.append(cur[:])
                return
            lo = need * (2 * nxt + need - 1) // 2       # nxt + ... + (nxt + need - 1)
            hi = need * (2 * m - need + 1) // 2         # (m - need + 1) + ... + m
            if left < lo or left > hi:
                return
            for t in range(nxt, m - need + 2):
                if t > left:
                    break
                cur.append(t)
                go(t + 1, need - 1, left - t)
                cur.pop()

        go(1, k, target)
        return out
