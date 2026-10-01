class Solution:
    def shortestFix(self, s):
        n = len(s)
        q = n // 4
        out = {c: 0 for c in "SATB"}
        for c in s:
            out[c] += 1
        if all(v == q for v in out.values()):
            return 0
        best = n
        left = 0
        for i, c in enumerate(s):
            out[c] -= 1
            while left <= i and all(v <= q for v in out.values()):
                best = min(best, i - left + 1)
                out[s[left]] += 1
                left += 1
        return best
