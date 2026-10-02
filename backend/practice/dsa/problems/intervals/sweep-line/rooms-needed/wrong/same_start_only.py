class Solution:
    # Mistake: counts the most meetings that START at the same time.
    def roomsNeeded(self, meetings):
        from collections import Counter
        return max(Counter(s for s, _ in meetings).values())
