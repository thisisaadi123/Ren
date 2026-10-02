class Solution:
    # Mistake: won't go to a talk that starts exactly when the last one ends.
    def mostTalks(self, talks):
        count, free = 0, -1
        for s, e in sorted(talks, key=lambda t: t[1]):
            if s > free:
                count += 1
                free = e
        return count
