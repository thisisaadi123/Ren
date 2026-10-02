class Solution:
    # Mistake: adds up the whole connected patch of gold, as if branches could be walked without backtracking.
    def mostGold(self, mine):
        m, n = len(mine), len(mine[0])
        seen, best = set(), 0
        for r0 in range(m):
            for c0 in range(n):
                if mine[r0][c0] and (r0, c0) not in seen:
                    stack, total = [(r0, c0)], 0
                    seen.add((r0, c0))
                    while stack:
                        r, c = stack.pop()
                        total += mine[r][c]
                        for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                            if 0 <= rr < m and 0 <= cc < n and mine[rr][cc] and (rr, cc) not in seen:
                                seen.add((rr, cc))
                                stack.append((rr, cc))
                    best = max(best, total)
        return best
