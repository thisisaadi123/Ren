class Solution:
    # Mistake: treats equal beads as different, so repeated colours give repeated sequences.
    def beadOrders(self, beads):
        n = len(beads)
        used = [False] * n
        out, cur = [], []
        def go():
            if len(cur) == n:
                out.append(cur[:])
                return
            for i in range(n):
                if not used[i]:
                    used[i] = True
                    cur.append(beads[i])
                    go()
                    cur.pop()
                    used[i] = False
        go()
        return out
