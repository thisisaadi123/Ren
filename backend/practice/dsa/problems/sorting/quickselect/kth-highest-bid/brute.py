class Solution:
    def kthHighest(self, bids, k):
        return sorted(bids, reverse=True)[k - 1]
