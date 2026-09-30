class Solution:
    def feudFreeLists(self, ages, k):
        n = len(ages)
        good = 0
        for mask in range(1, 1 << n):
            pick = [ages[i] for i in range(n) if mask >> i & 1]
            if all(abs(x - y) != k for x in pick for y in pick):
                good += 1
        return good
