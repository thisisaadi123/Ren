class Solution:
    def nextGate(self, gates, current):
        lo, hi = 0, len(gates)
        while lo < hi:
            mid = (lo + hi) // 2
            if gates[mid] <= current:
                lo = mid + 1
            else:
                hi = mid
        return gates[lo % len(gates)]
