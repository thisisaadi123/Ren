class Solution:
    def straightWords(self, board, words):
        m, n = len(board), len(board[0])
        dirs = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]

        def hidden(w):
            for r in range(m):
                for c in range(n):
                    for dr, dc in dirs:
                        if all(0 <= r + i * dr < m and 0 <= c + i * dc < n and board[r + i * dr][c + i * dc] == w[i] for i in range(len(w))):
                            return True
            return False

        return sorted(w for w in set(words) if hidden(w))
