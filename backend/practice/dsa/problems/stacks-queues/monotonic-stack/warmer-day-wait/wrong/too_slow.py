class Solution:
    # Mistake: scans forward from every day: O(n²) when warmer days are far away or missing.
    def daysUntilWarmer(self, temps):
        n = len(temps)
        res = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if temps[j] > temps[i]:
                    res[i] = j - i
                    break
        return res
