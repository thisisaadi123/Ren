class Solution:
    # Mistake: keeps the later window on a tie.
    def trailWindow(self, s, t):
        m = len(t)
        start = [-1] * (m + 1)
        best_len, best_start = len(s) + 1, 0
        for i, c in enumerate(s):
            for j in range(m, 0, -1):
                if t[j - 1] == c:
                    start[j] = i if j == 1 else start[j - 1]
            if start[m] >= 0 and i - start[m] + 1 <= best_len:
                best_len, best_start = i - start[m] + 1, start[m]
        return s[best_start:best_start + best_len] if best_len <= len(s) else ""
