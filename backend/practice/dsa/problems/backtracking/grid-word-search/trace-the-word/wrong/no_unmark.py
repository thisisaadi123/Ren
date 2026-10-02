class Solution:
    # Mistake: forgets to unmark a cell when a path fails, so later paths can't use it.
    def traceWord(self, board, word):
        m, n = len(board), len(board[0])
        used = [[False] * n for _ in range(m)]

        def go(r, c, i):
            if board[r][c] != word[i]:
                return False
            if i == len(word) - 1:
                return True
            used[r][c] = True
            return any(0 <= rr < m and 0 <= cc < n and not used[rr][cc] and go(rr, cc, i + 1) for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))

        return any(go(r, c, 0) for r in range(m) for c in range(n))
