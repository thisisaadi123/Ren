class Solution:
    def roomsNeeded(self, meetings):
        return max(sum(1 for s, e in meetings if s <= t < e) for t, _ in meetings)
