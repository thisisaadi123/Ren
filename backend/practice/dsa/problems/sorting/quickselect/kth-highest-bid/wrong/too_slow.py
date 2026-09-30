class Solution:
    def kthHighest(self, bids, k):
        a = bids[:]
        for _ in range(k - 1):
            a.remove(max(a))
        return max(a)
