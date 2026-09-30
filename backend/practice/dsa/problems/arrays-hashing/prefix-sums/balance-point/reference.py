class Solution:
    def balancePoint(self, weights):
        total, left = sum(weights), 0
        for i, w in enumerate(weights):
            if left == total - left - w:
                return i
            left += w
        return -1
