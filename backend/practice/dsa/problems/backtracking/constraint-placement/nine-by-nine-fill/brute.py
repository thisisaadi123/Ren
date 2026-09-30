class Solution:
    def fillGrid(self, board):
        g = [row[:] for row in board]
        def ok(r, c, d):
            for i in range(9):
                if g[r][i] == d or g[i][c] == d:
                    return False
            br, bc = r // 3 * 3, c // 3 * 3
            return all(g[i][j] != d for i in range(br, br + 3) for j in range(bc, bc + 3))
        def go(p):
            while p < 81 and g[p // 9][p % 9] != ".":
                p += 1
            if p == 81:
                return True
            r, c = divmod(p, 9)
            for d in "123456789":
                if ok(r, c, d):
                    g[r][c] = d
                    if go(p + 1):
                        return True
                    g[r][c] = "."
            return False
        go(0)
        return g
