class Solution:
    # Mistake: walks every stretch: O(n^2).
    def totalSwing(self, readings):
        n = len(readings)
        total = 0
        for i in range(n):
            hi = lo = readings[i]
            for j in range(i, n):
                v = readings[j]
                if v > hi:
                    hi = v
                elif v < lo:
                    lo = v
                total += hi - lo
        return total
