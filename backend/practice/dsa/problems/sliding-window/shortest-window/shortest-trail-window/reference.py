class Solution:
    def trailWindow(self, s, t):
        m = len(t)
        start = [-1] * (m + 1)
        at = {}
        for j, c in enumerate(t):
            at.setdefault(c, []).append(j + 1)
        for js in at.values():
            js.reverse()
        best_len, best_start = len(s) + 1, 0
        for i, c in enumerate(s):
            js = at.get(c)
            if not js:
                continue
            for j in js:
                start[j] = i if j == 1 else start[j - 1]
            if start[m] >= 0 and i - start[m] + 1 < best_len:
                best_len, best_start = i - start[m] + 1, start[m]
        return s[best_start:best_start + best_len] if best_len <= len(s) else ""
