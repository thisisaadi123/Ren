class Solution:
    # Mistake: records the working list itself, so every answer ends up as the same (empty) list.
    def mirrorCuts(self, s):
        out, cur = [], []

        def go(i):
            if i == len(s):
                out.append(cur)
                return
            for j in range(i + 1, len(s) + 1):
                piece = s[i:j]
                if piece == piece[::-1]:
                    cur.append(piece)
                    go(j)
                    cur.pop()

        go(0)
        return sorted(out)
