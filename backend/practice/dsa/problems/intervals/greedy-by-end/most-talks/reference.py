class Solution:
    def mostTalks(self, talks):
        count, free = 0, -1
        for s, e in sorted(talks, key=lambda t: t[1]):
            if s >= free:
                count += 1
                free = e
        return count
