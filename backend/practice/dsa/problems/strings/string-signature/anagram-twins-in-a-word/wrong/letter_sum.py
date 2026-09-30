class Solution:
    # Mistake: keys a substring by the sum of its letter codes, so "ad" and "bc" collide.
    def anagramTwins(self, s):
        n, total = len(s), 0
        for L in range(1, n):
            seen = collections.Counter(sum(map(ord, s[i:i + L])) for i in range(n - L + 1))
            total += sum(c * (c - 1) // 2 for c in seen.values())
        return total
