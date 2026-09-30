class Solution:
    # Mistake: treats k as 0-indexed.
    def kthOfTwo(self, a, b, k):
        c = sorted(a + b)
        return c[min(k, len(c) - 1)]
