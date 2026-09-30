class Solution:
    # Mistake: uses the "skip if equal to the previous unused bead" rule without sorting first,
    # so equal beads that aren't adjacent in the input still produce duplicates.
    def beadOrders(self, beads):
        b = beads
        n = len(b)
        used = [False] * n
        out, cur = [], []
        def go():
            if len(cur) == n:
                out.append(cur[:])
                return
            for i in range(n):
                if used[i] or (i > 0 and b[i] == b[i - 1] and not used[i - 1]):
                    continue
                used[i] = True
                cur.append(b[i])
                go()
                cur.pop()
                used[i] = False
        go()
        return out
