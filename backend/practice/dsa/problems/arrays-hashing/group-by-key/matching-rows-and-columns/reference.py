class Solution:
    def countMatchingPairs(self, grid):
        rows = collections.Counter(tuple(r) for r in grid)
        return sum(rows[col] for col in zip(*grid))
