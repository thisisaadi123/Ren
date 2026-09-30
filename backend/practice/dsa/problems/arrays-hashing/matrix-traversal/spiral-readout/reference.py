class Solution:
    def spiralOrder(self, grid):
        top, bottom, left, right = 0, len(grid) - 1, 0, len(grid[0]) - 1
        out = []
        while top <= bottom and left <= right:
            out += grid[top][left : right + 1]
            top += 1
            out += [grid[r][right] for r in range(top, bottom + 1)]
            right -= 1
            if top <= bottom:
                out += grid[bottom][left : right + 1][::-1]
                bottom -= 1
            if left <= right:
                out += [grid[r][left] for r in range(bottom, top - 1, -1)]
                left += 1
        return out
