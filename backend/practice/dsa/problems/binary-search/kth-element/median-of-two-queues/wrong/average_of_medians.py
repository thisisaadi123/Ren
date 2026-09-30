class Solution:
    # Mistake: averages the two lists' own medians.
    def combinedMedian(self, a, b):
        def med(c):
            n = len(c)
            return c[n // 2] if n % 2 else (c[n // 2 - 1] + c[n // 2]) / 2
        if not a:
            return float(med(b))
        if not b:
            return float(med(a))
        return (med(a) + med(b)) / 2
