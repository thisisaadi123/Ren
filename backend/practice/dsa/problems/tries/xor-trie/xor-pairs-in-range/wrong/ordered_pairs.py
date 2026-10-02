class Solution:
    # Mistake: counts (i, j) and (j, i) separately.
    def xorPairsInRange(self, nums, low, high):
        from collections import Counter
        c = Counter(nums)
        total = 0
        for a in c:
            for b in c:
                if a != b and low <= a ^ b <= high:
                    total += c[a] * c[b]
        return total
