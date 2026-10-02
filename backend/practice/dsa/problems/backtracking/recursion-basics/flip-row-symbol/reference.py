class Solution:
    def symbolAt(self, n, k):
        if n == 1:
            return 0
        p = self.symbolAt(n - 1, (k + 1) // 2)
        return p if k % 2 else 1 - p
