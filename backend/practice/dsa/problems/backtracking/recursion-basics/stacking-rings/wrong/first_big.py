class Solution:
    # Mistake: moves the biggest ring before clearing the smaller ones off it.
    def ringMoves(self, n):
        out = []

        def move(k, a, b, c):
            if k:
                out.append([a, b])
                move(k - 1, a, c, b)
                move(k - 1, c, b, a)

        move(n, 1, 3, 2)
        return out
