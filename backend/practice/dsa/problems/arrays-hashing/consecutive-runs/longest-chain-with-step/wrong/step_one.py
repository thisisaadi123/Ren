class Solution:
    # Mistake: ignores the step and looks for consecutive numbers.
    def longestChain(self, values, step):
        have = set(values)
        best = 0
        for v in have:
            if v - 1 not in have:
                length = 1
                while v + length in have:
                    length += 1
                best = max(best, length)
        return best
