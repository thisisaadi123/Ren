class Solution:
    # Mistake: only skips taken numbers smaller than k itself.
    def kthFree(self, taken, k):
        return k + sum(1 for t in taken if t <= k)
