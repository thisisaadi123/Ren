class Solution:
    # Mistake: also allows diagonal moves.
    def wordHunt(self, board, words):
        m, n = len(board), len(board[0])
        steps = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]

        def can(w):
            def go(r, c, i, used):
                if board[r][c] != w[i]:
                    return False
                if i == len(w) - 1:
                    return True
                used.add((r, c))
                ok = any(0 <= r + a < m and 0 <= c + b < n and (r + a, c + b) not in used and go(r + a, c + b, i + 1, used) for a, b in steps)
                used.discard((r, c))
                return ok

            return any(go(r, c, 0, set()) for r in range(m) for c in range(n))

        return sorted(w for w in set(words) if can(w))
