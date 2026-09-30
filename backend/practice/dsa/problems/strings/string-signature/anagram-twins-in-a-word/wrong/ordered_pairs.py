class Solution:
    # Mistake: counts each pair twice, once in each order.
    def anagramTwins(self, s):
        n, total = len(s), 0
        for L in range(1, n):
            seen = collections.Counter("".join(sorted(s[i:i + L])) for i in range(n - L + 1))
            total += sum(c * (c - 1) for c in seen.values())
        return total
