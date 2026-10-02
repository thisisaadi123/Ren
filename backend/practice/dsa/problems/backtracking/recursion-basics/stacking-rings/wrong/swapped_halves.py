class Solution:
    # Mistake: parks the smaller rings on the target instead of the spare peg.
    def ringMoves(self, n):
        out = []

        def move(k, a, b, c):
            if k:
                move(k - 1, a, b, c)
                out.append([a, b])
                move(k - 1, c, b, a)

        move(n, 1, 3, 2)
        return out
