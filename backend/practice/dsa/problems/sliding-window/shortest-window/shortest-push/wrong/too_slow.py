class Solution:
    # Mistake: extends from every start: O(n^2) when the target is out of reach.
    def shortestPush(self, gains, target):
        n = len(gains)
        best = n + 1
        for i in range(n):
            t = 0
            for j in range(i, n):
                t += gains[j]
                if t >= target:
                    best = min(best, j - i + 1)
                    break
        return best if best <= n else 0
