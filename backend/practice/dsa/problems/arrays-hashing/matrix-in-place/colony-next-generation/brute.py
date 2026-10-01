class Solution:
    def nextGeneration(self, board):
        m, n = len(board), len(board[0])
        out = [[0] * n for _ in range(m)]
        for r in range(m):
            for c in range(n):
                live = sum(board[r + dr][c + dc]
                           for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                           if (dr, dc) != (0, 0) and 0 <= r + dr < m and 0 <= c + dc < n)
                if board[r][c] == 1:
                    out[r][c] = 1 if live in (2, 3) else 0
                else:
                    out[r][c] = 1 if live == 3 else 0
        return out
