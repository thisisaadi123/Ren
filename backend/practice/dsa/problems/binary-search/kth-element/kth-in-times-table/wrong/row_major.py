class Solution:
    # Mistake: assumes the table read row by row is sorted.
    def kthInTable(self, rows, cols, k):
        i, j = divmod(k - 1, cols)
        return (i + 1) * (j + 1)
