from collections import Counter


class Solution:
    def coverWindow(self, s, t):
        want = Counter(t)
        for length in range(len(t), len(s) + 1):
            for i in range(len(s) - length + 1):
                part = Counter(s[i:i + length])
                if all(part[c] >= k for c, k in want.items()):
                    return s[i:i + length]
        return ""
