class Solution:
    def countUnderCap(self, factors, cap):
        n = len(factors)
        total = 0
        for i in range(n):
            p = 1
            for j in range(i, n):
                p *= factors[j]
                if p < cap:
                    total += 1
        return total
