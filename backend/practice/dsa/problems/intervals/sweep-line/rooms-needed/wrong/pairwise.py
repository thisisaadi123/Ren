class Solution:
    # Mistake: counts only meetings that overlap the first meeting of the day.
    def roomsNeeded(self, meetings):
        ms = sorted(meetings)
        s0, e0 = ms[0]
        return 1 + sum(1 for s, e in ms[1:] if s < e0)
