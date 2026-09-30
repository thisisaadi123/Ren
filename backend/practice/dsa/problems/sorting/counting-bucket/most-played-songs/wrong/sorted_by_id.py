import collections
class Solution:
    # Mistake: returns the right songs but in id order.
    def mostPlayed(self, plays, k):
        count = collections.Counter(plays)
        return sorted(sorted(count, key=lambda s: (-count[s], s))[:k])
