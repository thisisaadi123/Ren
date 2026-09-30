class Solution:
    def combinedMedian(self, a, b):
        c = sorted(a + b)
        n = len(c)
        return float(c[n // 2]) if n % 2 else (c[n // 2 - 1] + c[n // 2]) / 2
