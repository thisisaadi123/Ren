class Solution:
    def mostScoops(self, flavours):
        n = len(flavours)
        best = 0
        for i in range(n):
            for j in range(i, n):
                if len(set(flavours[i:j + 1])) <= 2:
                    best = max(best, j - i + 1)
        return best
