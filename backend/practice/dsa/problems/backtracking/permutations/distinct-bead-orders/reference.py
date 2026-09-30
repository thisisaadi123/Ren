class Solution:
    def beadOrders(self, beads):
        left = collections.Counter(beads)
        colours = sorted(left)
        n = len(beads)
        out, cur = [], []

        def go():
            if len(cur) == n:
                out.append(cur[:])
                return
            for c in colours:
                if left[c]:
                    left[c] -= 1
                    cur.append(c)
                    go()
                    cur.pop()
                    left[c] += 1

        go()
        return out
