class Solution:
    # Mistake: picks the talk that starts first, which may run very long.
    def mostTalks(self, talks):
        count, free = 0, -1
        for s, e in sorted(talks):
            if s >= free:
                count += 1
                free = e
        return count
