class Solution:
    def daysUntilWarmer(self, temps):
        n = len(temps)
        res = []
        for i in range(n):
            res.append(next((j - i for j in range(i + 1, n) if temps[j] > temps[i]), 0))
        return res
