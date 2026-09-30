class Solution:
    def topGenres(self, plays, k):
        count = collections.Counter(plays)
        return sorted(count, key=lambda g: (-count[g], g))[:k]
