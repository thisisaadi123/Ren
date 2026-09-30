class Solution:
    # Mistake: counts only neighbouring pairs.
    def countOutOfOrder(self, ranks):
        return sum(1 for i in range(len(ranks) - 1) if ranks[i] > ranks[i + 1])
