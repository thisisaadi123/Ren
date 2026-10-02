class Solution:
    # Mistake: ignores the rule that both teams have exactly n players.
    def smallestGap(self, skills):
        total = sum(skills)
        sums = {0}
        for x in skills:
            sums |= {s + x for s in sums}
        return min(abs(total - 2 * s) for s in sums)
