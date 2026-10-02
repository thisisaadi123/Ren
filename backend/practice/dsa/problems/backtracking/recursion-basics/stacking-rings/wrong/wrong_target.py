class Solution:
    # Mistake: moves the rings to peg 2 instead of peg 3.
    def ringMoves(self, n):
        out = []

        def move(k, a, b, c):
            if k:
                move(k - 1, a, c, b)
                out.append([a, b])
                move(k - 1, c, b, a)

        move(n, 1, 2, 3)
        return out
