class Solution:
    # Mistake: skips repeated bids.
    def kthHighest(self, bids, k):
        s = sorted(set(bids), reverse=True)
        return s[min(k, len(s)) - 1]
