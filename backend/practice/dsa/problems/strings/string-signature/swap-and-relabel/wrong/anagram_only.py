class Solution:
    # Mistake: only allows swaps, as if relabelling weren't a move.
    def canReshape(self, a, b):
        return collections.Counter(a) == collections.Counter(b)
