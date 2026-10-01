class Solution:
    # Mistake: ignores that the table is round, so groups across the ends aren't considered.
    def fewestSwaps(self, seats):
        n, t = len(seats), sum(seats)
        if t == 0:
            return 0
        inside = sum(seats[:t])
        best = inside
        for i in range(t, n):
            inside += seats[i] - seats[i - t]
            best = max(best, inside)
        return t - best
