class Solution:
    def minSwapsThreeColours(self, balls):
        s = sorted(balls)
        c = [[0] * 3 for _ in range(3)]
        for have, want in zip(balls, s):
            c[have][want] += 1
        moves = 0
        for a in range(3):
            for b in range(a + 1, 3):
                m = min(c[a][b], c[b][a])
                moves += m
                c[a][b] -= m
                c[b][a] -= m
        leftover = sum(c[a][b] for a in range(3) for b in range(3) if a != b)
        return moves + 2 * leftover // 3
