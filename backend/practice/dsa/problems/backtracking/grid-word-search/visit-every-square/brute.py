class Solution:
    def tourCount(self, floor):
        m, n = len(floor), len(floor[0])
        cells = {(r, c) for r in range(m) for c in range(n) if floor[r][c] != -1}
        start = next(p for p in cells if floor[p[0]][p[1]] == 1)
        count = 0
        stack = [(start, frozenset([start]))]
        while stack:
            (r, c), seen = stack.pop()
            if floor[r][c] == 2:
                count += len(seen) == len(cells)
                continue
            for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if nb in cells and nb not in seen:
                    stack.append((nb, seen | {nb}))
        return count
