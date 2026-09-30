class Solution:
    # Mistake: swap-based, but the loop starts at i + 1, so a float never stays in its own slot.
    def lineUps(self, floats):
        a = floats[:]
        n = len(a)
        out = []
        def go(i):
            if i >= n - 1:
                out.append(a[:])
                return
            for j in range(i + 1, n):
                a[i], a[j] = a[j], a[i]
                go(i + 1)
                a[i], a[j] = a[j], a[i]
        go(0)
        return out
