class Solution:
    # Mistake: only looks at the lower 30 bits.
    def bestXor(self, nums):
        best = 0
        mask = 0
        for bit in range(29, -1, -1):
            mask |= 1 << bit
            prefixes = {x & mask for x in nums}
            want = best | (1 << bit)
            if any(want ^ p in prefixes for p in prefixes):
                best = want
        return best
