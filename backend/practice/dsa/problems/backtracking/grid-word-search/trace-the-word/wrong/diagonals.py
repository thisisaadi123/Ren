class Solution:
    # Mistake: also allows diagonal steps.
    def traceWord(self, board, word):
        m, n = len(board), len(board[0])
        used = [[False] * n for _ in range(m)]

        def go(r, c, i):
            if board[r][c] != word[i]:
                return False
            if i == len(word) - 1:
                return True
            used[r][c] = True
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if (dr or dc) and 0 <= rr < m and 0 <= cc < n and not used[rr][cc] and go(rr, cc, i + 1):
                        used[r][c] = False
                        return True
            used[r][c] = False
            return False

        return any(go(r, c, 0) for r in range(m) for c in range(n))
