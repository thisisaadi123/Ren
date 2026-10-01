class Solution:
    # Mistake: recounts every run of t seats: O(n * t).
    def fewestSwaps(self, seats):
        n, t = len(seats), sum(seats)
        if t == 0:
            return 0
        best = 0
        for s in range(n):
            w = 0
            for j in range(t):
                w += seats[(s + j) % n]
            best = max(best, w)
        return t - best
