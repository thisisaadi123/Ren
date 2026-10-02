class Solution:
    # Mistake: lets a word use the same cell more than once.
    def wordHunt(self, board, words):
        m, n = len(board), len(board[0])

        def can(w):
            cur = {(r, c) for r in range(m) for c in range(n) if board[r][c] == w[0]}
            for ch in w[1:]:
                cur = {(rr, cc) for r, c in cur for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
                       if 0 <= rr < m and 0 <= cc < n and board[rr][cc] == ch}
            return bool(cur)

        return sorted(w for w in set(words) if can(w))
