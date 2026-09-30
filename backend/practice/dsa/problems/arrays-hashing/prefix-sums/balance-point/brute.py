class Solution:
    def balancePoint(self, weights):
        for i in range(len(weights)):
            if sum(weights[:i]) == sum(weights[i + 1:]):
                return i
        return -1
