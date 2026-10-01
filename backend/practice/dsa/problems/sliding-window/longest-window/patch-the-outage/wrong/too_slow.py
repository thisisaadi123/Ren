class Solution:
    # Mistake: extends from every start: O(n^2) when k is large.
    def longestOnline(self, status, k):
        n = len(status)
        best = 0
        for i in range(n):
            z = 0
            for j in range(i, n):
                z += status[j] == 0
                if z > k:
                    break
                best = max(best, j - i + 1)
        return best
