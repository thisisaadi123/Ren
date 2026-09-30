class Solution:
    # Mistake: hard-codes tiles 1 to 9 (the digits), ignoring m.
    def tileSums(self, m, k, target):
        out, cur = [], []
        def go(nxt, need, left):
            if need == 0:
                if left == 0:
                    out.append(cur[:])
                return
            for t in range(nxt, 10):
                if t > left:
                    break
                cur.append(t)
                go(t + 1, need - 1, left - t)
                cur.pop()
        go(1, k, target)
        return out
