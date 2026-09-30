class Solution:
    # Mistake: skips a bead whenever it equals the previous one, even if that one is already threaded,
    # so orders that put two equal beads side by side can never be built.
    def beadOrders(self, beads):
        b = sorted(beads)
        n = len(b)
        used = [False] * n
        out, cur = [], []
        def go():
            if len(cur) == n:
                out.append(cur[:])
                return
            for i in range(n):
                if used[i] or (i > 0 and b[i] == b[i - 1]):
                    continue
                used[i] = True
                cur.append(b[i])
                go()
                cur.pop()
                used[i] = False
        go()
        return out
