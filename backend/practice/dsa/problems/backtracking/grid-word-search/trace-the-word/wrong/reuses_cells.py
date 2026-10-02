class Solution:
    # Mistake: never marks cells as used, so a path can step back onto itself.
    def traceWord(self, board, word):
        m, n = len(board), len(board[0])

        def go(r, c, i):
            if board[r][c] != word[i]:
                return False
            if i == len(word) - 1:
                return True
            return any(0 <= rr < m and 0 <= cc < n and go(rr, cc, i + 1) for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))

        return any(go(r, c, 0) for r in range(m) for c in range(n))
