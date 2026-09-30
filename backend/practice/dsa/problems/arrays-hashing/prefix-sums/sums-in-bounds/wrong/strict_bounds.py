class Solution:
    # Mistake: excludes sums equal to lower or upper.
    def countSumsInBounds(self, nums, lower, upper):
        prefix, seen, total = 0, collections.Counter({0: 1}), 0
        for x in nums:
            prefix += x
            total += sum(c for p, c in seen.items() if lower < prefix - p < upper)
            seen[prefix] += 1
        return total
