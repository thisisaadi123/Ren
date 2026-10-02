class Solution:
    def mostPieces(self, s):
        n = len(s)
        best = [0]
        used = set()

        def go(i):
            if len(used) + (n - i) <= best[0]:
                return
            if i == n:
                best[0] = max(best[0], len(used))
                return
            for j in range(i + 1, n + 1):
                p = s[i:j]
                if p not in used:
                    used.add(p)
                    go(j)
                    used.remove(p)

        go(0)
        return best[0]
