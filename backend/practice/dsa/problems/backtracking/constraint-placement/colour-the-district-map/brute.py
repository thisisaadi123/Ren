import itertools
class Solution:
    def canColour(self, n, borders, m):
        for cols in itertools.product(range(m), repeat=n):
            if all(cols[a] != cols[b] for a, b in borders):
                return True
        return False
