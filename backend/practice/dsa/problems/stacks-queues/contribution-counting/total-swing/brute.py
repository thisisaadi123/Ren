class Solution:
    def totalSwing(self, readings):
        n = len(readings)
        total = 0
        for i in range(n):
            hi = lo = readings[i]
            for j in range(i, n):
                hi = max(hi, readings[j])
                lo = min(lo, readings[j])
                total += hi - lo
        return total
