class Solution:
    # Mistake: simulates the circle by stepping one person at a time.
    def lastSeat(self, n, k):
        alive, left, at = [True] * n, n, 0
        while left > 1:
            steps = k
            while True:
                if alive[at]:
                    steps -= 1
                    if steps == 0:
                        break
                at = (at + 1) % n
            alive[at] = False
            left -= 1
        return alive.index(True) + 1
