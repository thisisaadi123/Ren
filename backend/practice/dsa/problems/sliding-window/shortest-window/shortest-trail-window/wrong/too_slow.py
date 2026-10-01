class Solution:
    # Mistake: from every start, matches forward to the end of t: O(n^2) when t's last letter is far away.
    def trailWindow(self, s, t):
        best_len, best_start = len(s) + 1, 0
        for i in range(len(s)):
            if s[i] != t[0]:
                continue
            k = 0
            for j in range(i, len(s)):
                if s[j] == t[k]:
                    k += 1
                    if k == len(t):
                        if j - i + 1 < best_len:
                            best_len, best_start = j - i + 1, i
                        break
        return s[best_start:best_start + best_len] if best_len <= len(s) else ""
