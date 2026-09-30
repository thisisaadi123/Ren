class Solution:
    # Mistake: fills from the front with the smaller end.
    def sortedSquares(self, values):
        out = []
        i, j = 0, len(values) - 1
        while i <= j:
            if abs(values[i]) < abs(values[j]):
                out.append(values[i] ** 2); i += 1
            else:
                out.append(values[j] ** 2); j -= 1
        return out
