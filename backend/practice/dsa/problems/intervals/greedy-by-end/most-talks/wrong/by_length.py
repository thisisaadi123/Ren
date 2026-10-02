class Solution:
    # Mistake: picks the shortest talks first.
    def mostTalks(self, talks):
        chosen = []
        for s, e in sorted(talks, key=lambda t: t[1] - t[0]):
            if all(e <= a or s >= b for a, b in chosen):
                chosen.append((s, e))
        return len(chosen)
