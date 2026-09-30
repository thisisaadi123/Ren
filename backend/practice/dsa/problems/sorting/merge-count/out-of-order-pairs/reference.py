class Solution:
    def countOutOfOrder(self, ranks):
        n = len(ranks)
        return sum(1 for i in range(n) for j in range(i + 1, n) if ranks[i] > ranks[j])
