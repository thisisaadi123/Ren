class Solution:
    # Mistake: sorts by count the wrong way round.
    def topGenres(self, plays, k):
        count = collections.Counter(plays)
        return sorted(count, key=lambda g: (count[g], g))[:k]
