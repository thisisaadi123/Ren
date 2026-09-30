class Solution:
    def topGenres(self, plays, k):
        left = sorted(set(plays))
        out = []
        for _ in range(k):
            best = max(left, key=lambda g: (plays.count(g), -g))
            out.append(best)
            left.remove(best)
        return out
