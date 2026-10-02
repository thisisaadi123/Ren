class Solution:
    # Mistake: lists a word once for every time it appears in words.
    def wordHunt(self, board, words):
        m, n = len(board), len(board[0])

        def can(w):
            def go(r, c, i, used):
                if board[r][c] != w[i]:
                    return False
                if i == len(w) - 1:
                    return True
                used.add((r, c))
                ok = any(0 <= rr < m and 0 <= cc < n and (rr, cc) not in used and go(rr, cc, i + 1, used)
                         for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
                used.discard((r, c))
                return ok

            return any(go(r, c, 0, set()) for r in range(m) for c in range(n))

        return sorted(w for w in words if can(w))
