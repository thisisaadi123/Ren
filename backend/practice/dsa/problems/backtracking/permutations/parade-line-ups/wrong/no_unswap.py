class Solution:
    # Mistake: swaps a float into place but never swaps it back, so later branches start from a scrambled row.
    def lineUps(self, floats):
        a = floats[:]
        n = len(a)
        out = []
        def go(i):
            if i == n:
                out.append(a[:])
                return
            for j in range(i, n):
                a[i], a[j] = a[j], a[i]
                go(i + 1)
        go(0)
        return out
