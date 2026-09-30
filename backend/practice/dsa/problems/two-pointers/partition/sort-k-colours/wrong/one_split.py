class Solution:
    # Mistake: splits around the middle colour once but never sorts inside the halves.
    def sortKColours(self, balls, k):
        mid = (1 + k) // 2
        return [x for x in balls if x <= mid] + [x for x in balls if x > mid]
