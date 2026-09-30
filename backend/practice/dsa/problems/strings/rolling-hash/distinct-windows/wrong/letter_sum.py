class Solution:
    # Mistake: a sum of letters ignores order, so "ab" and "ba" collide.
    def distinctWindows(self, s, k):
        seen = set()
        h = sum(ord(c) for c in s[:k])
        seen.add(h)
        for i in range(k, len(s)):
            h += ord(s[i]) - ord(s[i - k])
            seen.add(h)
        return len(seen)
