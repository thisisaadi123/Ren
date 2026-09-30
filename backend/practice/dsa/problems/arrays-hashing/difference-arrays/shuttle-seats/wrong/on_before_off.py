class Solution:
    # Mistake: counts people getting off at a mark as still on board there.
    def canCarryAll(self, capacity, trips):
        change = [0] * (max(t[2] for t in trips) + 2)
        for p, a, b in trips:
            change[a] += p
            change[b + 1] -= p
        on_board = 0
        for c in change:
            on_board += c
            if on_board > capacity:
                return False
        return True
