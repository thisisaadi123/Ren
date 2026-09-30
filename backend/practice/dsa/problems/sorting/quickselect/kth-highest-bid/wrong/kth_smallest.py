class Solution:
    # Mistake: counts from the bottom.
    def kthHighest(self, bids, k):
        return sorted(bids)[k - 1]
