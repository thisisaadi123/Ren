class Solution:
    # Mistake: thinks a hole stops a queen's attack, so queens on opposite sides of a hole may share a line.
    def countQueens(self, n, holes):
        hole = {(r, c) for r, c in holes}
        placed = []
        def attacks(r1, c1, r2, c2):
            if c1 != c2 and abs(r1 - r2) != abs(c1 - c2):
                return False
            dr = (r2 > r1) - (r2 < r1)
            dc = (c2 > c1) - (c2 < c1)
            r, c = r1 + dr, c1 + dc
            while (r, c) != (r2, c2):
                if (r, c) in hole:
                    return False
                r += dr; c += dc
            return True
        def go(r):
            if r == n:
                return 1
            total = 0
            for c in range(n):
                if (r, c) in hole or any(attacks(pr, pc, r, c) for pr, pc in placed):
                    continue
                placed.append((r, c))
                total += go(r + 1)
                placed.pop()
            return total
        return go(0)
