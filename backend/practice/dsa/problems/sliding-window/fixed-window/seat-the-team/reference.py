class Solution:
    def fewestSwaps(self, seats):
        n, t = len(seats), sum(seats)
        if t == 0:
            return 0
        inside = sum(seats[:t])
        best = inside
        for i in range(t, n + t):
            inside += seats[i % n] - seats[(i - t) % n]
            best = max(best, inside)
        return t - best
