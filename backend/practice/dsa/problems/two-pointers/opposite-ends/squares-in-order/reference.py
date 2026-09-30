class Solution:
    def sortedSquares(self, values):
        n = len(values)
        out = [0] * n
        i, j = 0, n - 1
        for k in range(n - 1, -1, -1):
            if abs(values[i]) > abs(values[j]):
                out[k] = values[i] * values[i]
                i += 1
            else:
                out[k] = values[j] * values[j]
                j -= 1
        return out
