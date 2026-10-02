class Solution:
    def ringMoves(self, n):
        out = []

        def move(k, a, b, c):
            if k == 0:
                return
            move(k - 1, a, c, b)
            out.append([a, b])
            move(k - 1, c, b, a)

        move(n, 1, 3, 2)
        return out
