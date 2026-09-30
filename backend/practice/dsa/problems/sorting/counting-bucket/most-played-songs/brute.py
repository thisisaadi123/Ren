import collections
class Solution:
    def mostPlayed(self, plays, k):
        count = collections.Counter(plays)
        return sorted(count, key=lambda s: (-count[s], s))[:k]
