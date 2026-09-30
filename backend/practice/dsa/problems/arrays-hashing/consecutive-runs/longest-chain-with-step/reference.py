class Solution:
    def longestChain(self, values, step):
        have = set(values)
        best = 0
        for v in have:
            if v - step not in have:
                length, x = 1, v
                while x + step in have:
                    x += step
                    length += 1
                best = max(best, length)
        return best
