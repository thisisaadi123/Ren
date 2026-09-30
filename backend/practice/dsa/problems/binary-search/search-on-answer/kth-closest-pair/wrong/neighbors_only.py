class Solution:
    # Mistake: only considers gaps between neighbours after sorting.
    def kthPairGap(self, heights, k):
        h = sorted(heights)
        gaps = sorted(b - a for a, b in zip(h, h[1:]))
        return gaps[min(k, len(gaps)) - 1]
