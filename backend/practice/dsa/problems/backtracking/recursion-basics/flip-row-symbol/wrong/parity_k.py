class Solution:
    # Mistake: uses whether k is even instead of tracing back to the parent.
    def symbolAt(self, n, k):
        return 0 if k % 2 else 1
