class Solution:
    def longestUniform(self, s, k):
        best = 0
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                part = s[i:j]
                if len(part) - max(part.count(c) for c in set(part)) <= k:
                    best = max(best, j - i)
        return best
