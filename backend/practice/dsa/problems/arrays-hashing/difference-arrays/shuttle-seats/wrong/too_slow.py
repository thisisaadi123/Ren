class Solution:
    def canCarryAll(self, capacity, trips):
        last = max(t[2] for t in trips)
        for mark in range(last + 1):
            if sum(p for p, a, b in trips if a <= mark < b) > capacity:
                return False
        return True
