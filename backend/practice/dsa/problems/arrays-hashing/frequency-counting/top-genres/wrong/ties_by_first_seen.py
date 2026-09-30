class Solution:
    # Mistake: breaks ties by which genre appeared first, not by the smaller id.
    def topGenres(self, plays, k):
        return [g for g, _ in collections.Counter(plays).most_common(k)]
