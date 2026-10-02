class Solution:
    # Mistake: treats k as 0-indexed.
    def symbolAt(self, n, k):
        return bin(k).count("1") % 2
