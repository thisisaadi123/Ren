class Solution:
    def mostServed(self, customers, moody, minutes):
        n = len(customers)
        best = 0
        for start in range(n - minutes + 1):
            happy = sum(customers[i] for i in range(n) if not moody[i] or start <= i < start + minutes)
            best = max(best, happy)
        return best
