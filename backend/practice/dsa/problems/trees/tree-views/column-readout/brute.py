class Solution:
    def columnReadout(self, root):
        grid = {}

        def walk(t, r, c):
            if t:
                grid.setdefault(c, {}).setdefault(r, []).append(t.val)
                walk(t.left, r + 1, c - 1)
                walk(t.right, r + 1, c + 1)

        walk(root, 0, 0)
        return [[v for r in sorted(grid[c]) for v in sorted(grid[c][r])] for c in sorted(grid)]
