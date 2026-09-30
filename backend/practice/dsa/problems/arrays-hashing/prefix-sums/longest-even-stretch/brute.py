class Solution:
    def longestEvenStretch(self, bits):
        n, best = len(bits), 0
        for i in range(n):
            for j in range(i, n):
                seg = bits[i : j + 1]
                if seg.count(0) == seg.count(1):
                    best = max(best, j - i + 1)
        return best
