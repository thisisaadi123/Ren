class Solution:
    def closestTriple(self, values, target):
        n = len(values)
        best = None
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    s = values[i] + values[j] + values[k]
                    if best is None or (abs(s - target), s) < (abs(best - target), best):
                        best = s
        return best
