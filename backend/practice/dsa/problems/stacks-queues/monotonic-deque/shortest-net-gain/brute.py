class Solution:
    def shortestNetGain(self, changes, target):
        n = len(changes)
        best = -1
        for i in range(n):
            s = 0
            for j in range(i, n):
                s += changes[j]
                if s >= target and (best < 0 or j - i + 1 < best):
                    best = j - i + 1
        return best
