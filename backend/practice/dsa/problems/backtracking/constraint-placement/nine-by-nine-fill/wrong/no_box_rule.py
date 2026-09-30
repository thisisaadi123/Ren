class Solution:
    # Mistake: checks rows and columns but forgets the 3 x 3 boxes.
    def fillGrid(self, board):
        g = [row[:] for row in board]
        cells = [(r, c) for r in range(9) for c in range(9) if g[r][c] == "."]
        def go(i):
            if i == len(cells):
                return True
            r, c = cells[i]
            used = set(g[r]) | {g[x][c] for x in range(9)}
            for d in "123456789":
                if d not in used:
                    g[r][c] = d
                    if go(i + 1):
                        return True
                    g[r][c] = "."
            return False
        go(0)
        return g
