class Solution:
    def sectionCounts(self, n, groups):
        out = [0] * n
        for l, r, people in groups:
            for i in range(l, r + 1):
                out[i] += people
        return out
