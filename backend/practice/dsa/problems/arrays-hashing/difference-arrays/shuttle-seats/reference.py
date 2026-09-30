class Solution:
    def canCarryAll(self, capacity, trips):
        change = [0] * (max(t[2] for t in trips) + 1)
        for p, a, b in trips:
            change[a] += p
            change[b] -= p
        on_board = 0
        for c in change:
            on_board += c
            if on_board > capacity:
                return False
        return True
