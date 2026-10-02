class Solution:
    # Mistake: returns the ways in the order found instead of sorted.
    def mirrorCuts(self, s):
        out, cur = [], []

        def go(i):
            if i == len(s):
                out.append(cur[:])
                return
            for j in range(len(s), i, -1):
                piece = s[i:j]
                if piece == piece[::-1]:
                    cur.append(piece)
                    go(j)
                    cur.pop()

        go(0)
        return out
