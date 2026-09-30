class Solution:
    # Mistake: counts every candidate by scanning the whole array, O(n^2).
    def findRepeat(self, tickets):
        n = len(tickets) - 1
        for v in range(n, 0, -1):
            c = 0
            for t in tickets:
                if t == v:
                    c += 1
            if c > 1:
                return v
        return -1
