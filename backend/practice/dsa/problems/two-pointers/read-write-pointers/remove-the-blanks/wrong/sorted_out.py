class Solution:
    # Mistake: loses the original order.
    def removeValue(self, cells, blank):
        return sorted(x for x in cells if x != blank)
