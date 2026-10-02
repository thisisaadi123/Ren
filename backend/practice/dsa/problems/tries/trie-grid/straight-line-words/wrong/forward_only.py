class Solution:
    # Mistake: only reads left-to-right, top-to-bottom and the down-right diagonal, never backwards.
    def straightWords(self, board, words):
        m, n = len(board), len(board[0])
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]

        def hidden(w):
            return any(all(0 <= r + i * dr < m and 0 <= c + i * dc < n and board[r + i * dr][c + i * dc] == w[i] for i in range(len(w)))
                       for r in range(m) for c in range(n) for dr, dc in dirs)

        return sorted(w for w in set(words) if hidden(w))
