class Solution:
    def longestChain(self, values, step):
        have = set(values)
        best = 0
        for v in have:
            length = 1
            while v + length * step in have:
                length += 1
            best = max(best, length)
        return best
