class Solution:
    # Mistake: treats high as exclusive.
    def xorPairsInRange(self, nums, low, high):
        from collections import Counter
        c = Counter(nums)
        keys = list(c)
        total = 0
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                if low <= a ^ b < high:
                    total += c[a] * c[b]
        return total
