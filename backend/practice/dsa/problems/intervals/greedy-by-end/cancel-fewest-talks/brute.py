from itertools import combinations


class Solution:
    def cancelFewest(self, talks):
        n = len(talks)
        for k in range(n, 0, -1):
            for pick in combinations(sorted(talks), k):
                if all(pick[i][1] <= pick[i + 1][0] for i in range(k - 1)):
                    return n - k
        return n
