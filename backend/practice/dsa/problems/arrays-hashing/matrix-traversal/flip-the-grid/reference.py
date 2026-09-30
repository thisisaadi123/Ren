class Solution:
    def transpose(self, grid):
        return [list(col) for col in zip(*grid)]
