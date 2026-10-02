class Solution:
    def roomsNeeded(self, meetings):
        starts = sorted(s for s, _ in meetings)
        ends = sorted(e for _, e in meetings)
        j = used = best = 0
        for s in starts:
            while ends[j] <= s:
                j += 1
                used -= 1
            used += 1
            best = max(best, used)
        return best
