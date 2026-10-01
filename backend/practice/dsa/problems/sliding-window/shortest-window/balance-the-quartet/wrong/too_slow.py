class Solution:
    # Mistake: grows a window from every start: O(n^2).
    def shortestFix(self, s):
        n = len(s)
        q = n // 4
        total = {c: s.count(c) for c in "SATB"}
        if all(v == q for v in total.values()):
            return 0
        best = n
        for i in range(n):
            out = dict(total)
            for j in range(i, n):
                out[s[j]] -= 1
                if out["S"] <= q and out["A"] <= q and out["T"] <= q and out["B"] <= q:
                    best = min(best, j - i + 1)
                    break
        return best
