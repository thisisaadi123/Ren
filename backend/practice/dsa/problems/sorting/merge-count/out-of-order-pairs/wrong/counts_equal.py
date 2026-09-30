class Solution:
    # Mistake: counts equal ranks as out of order.
    def countOutOfOrder(self, ranks):
        n = len(ranks)
        return sum(1 for i in range(n) for j in range(i + 1, n) if ranks[i] >= ranks[j])
