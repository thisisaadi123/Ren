from itertools import combinations


class Solution:
    def mostTalks(self, talks):
        for k in range(len(talks), 0, -1):
            for pick in combinations(sorted(talks), k):
                if all(pick[i][1] <= pick[i + 1][0] for i in range(k - 1)):
                    return k
        return 0
