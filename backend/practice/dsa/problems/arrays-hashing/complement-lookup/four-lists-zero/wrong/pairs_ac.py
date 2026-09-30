class Solution:
    # Mistake: only counts a + b + c + d with i == k and j == l.
    def countZeroQuads(self, a, b, c, d):
        return sum(1 for i in range(len(a)) for j in range(len(b)) if a[i] + b[j] + c[i] + d[j] == 0)
