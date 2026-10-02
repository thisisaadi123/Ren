class Solution:
    def wordHunt(self, board, words):
        m, n = len(board), len(board[0])

        def can(w):
            def go(r, c, i, used):
                if board[r][c] != w[i]:
                    return False
                if i == len(w) - 1:
                    return True
                used.add((r, c))
                for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= rr < m and 0 <= cc < n and (rr, cc) not in used and go(rr, cc, i + 1, used):
                        used.discard((r, c))
                        return True
                used.discard((r, c))
                return False

            return any(go(r, c, 0, set()) for r in range(m) for c in range(n))

        return sorted(w for w in set(words) if can(w))
