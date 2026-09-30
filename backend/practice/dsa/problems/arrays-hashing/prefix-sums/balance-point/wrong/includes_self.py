class Solution:
    # Mistake: counts weights[i] on the left side.
    def balancePoint(self, weights):
        total, left = sum(weights), 0
        for i, w in enumerate(weights):
            left += w
            if left == total - left:
                return i
        return -1
