class Solution:
    def maxNested(self, boxes):
        b = sorted(boxes, key=lambda x: (x[0], -x[1]))
        best = [1] * len(b)
        for i in range(len(b)):
            for j in range(i):
                if b[j][1] < b[i][1] and b[j][0] < b[i][0]:
                    best[i] = max(best[i], best[j] + 1)
        return max(best)
