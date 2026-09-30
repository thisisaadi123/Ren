class Solution:
    def longestEvenStretch(self, bits):
        n, best = len(bits), 0
        for i in range(n):
            t = 0
            for j in range(i, n):
                t += 1 if bits[j] else -1
                if t == 0:
                    best = max(best, j - i + 1)
        return best
