class Solution:
    def fewestSwaps(self, seats):
        n, t = len(seats), sum(seats)
        if t == 0:
            return 0
        return min(t - sum(seats[(s + j) % n] for j in range(t)) for s in range(n))
