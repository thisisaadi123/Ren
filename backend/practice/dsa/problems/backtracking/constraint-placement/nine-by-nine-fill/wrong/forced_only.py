class Solution:
    # Mistake: only fills cells with a single legal digit and stops when none is left; no guessing at all.
    def fillGrid(self, board):
        g = [row[:] for row in board]
        changed = True
        while changed:
            changed = False
            for r in range(9):
                for c in range(9):
                    if g[r][c] != ".":
                        continue
                    br, bc = r // 3 * 3, c // 3 * 3
                    used = set(g[r]) | {g[x][c] for x in range(9)} | {g[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
                    opts = [d for d in "123456789" if d not in used]
                    if len(opts) == 1:
                        g[r][c] = opts[0]
                        changed = True
        return g
