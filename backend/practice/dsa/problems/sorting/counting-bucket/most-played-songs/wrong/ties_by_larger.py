import collections
class Solution:
    # Mistake: breaks ties toward the larger id.
    def mostPlayed(self, plays, k):
        count = collections.Counter(plays)
        return sorted(count, key=lambda s: (-count[s], -s))[:k]
