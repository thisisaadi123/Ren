class Solution:
    def traceWord(self, board, word):
        m, n = len(board), len(board[0])
        paths = [[(r, c)] for r in range(m) for c in range(n) if board[r][c] == word[0]]
        for ch in word[1:]:
            nxt = []
            for p in paths:
                r, c = p[-1]
                for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= rr < m and 0 <= cc < n and (rr, cc) not in p and board[rr][cc] == ch:
                        nxt.append(p + [(rr, cc)])
            paths = nxt
        return bool(paths)
