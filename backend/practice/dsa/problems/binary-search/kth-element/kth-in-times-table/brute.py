class Solution:
    def kthInTable(self, rows, cols, k):
        return sorted(i * j for i in range(1, rows + 1) for j in range(1, cols + 1))[k - 1]
