class Solution:
    # Mistake: tries every start and scans right with a counter: O(n²).
    def longestBalanced(self, s):
        best, n = 0, len(s)
        for i in range(n):
            d = 0
            for j in range(i, n):
                d += 1 if s[j] == "(" else -1
                if d < 0:
                    break
                if d == 0:
                    best = max(best, j - i + 1)
        return best
