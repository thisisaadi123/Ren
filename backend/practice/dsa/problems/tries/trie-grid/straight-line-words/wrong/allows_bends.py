class Solution:
    # Mistake: lets the word turn corners, like a word hunt.
    def straightWords(self, board, words):
        m, n = len(board), len(board[0])
        dirs = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]

        def hidden(w):
            cur = {(r, c) for r in range(m) for c in range(n) if board[r][c] == w[0]}
            for ch in w[1:]:
                cur = {(r + a, c + b) for r, c in cur for a, b in dirs if 0 <= r + a < m and 0 <= c + b < n and board[r + a][c + b] == ch}
            return bool(cur)

        return sorted(w for w in set(words) if hidden(w))
