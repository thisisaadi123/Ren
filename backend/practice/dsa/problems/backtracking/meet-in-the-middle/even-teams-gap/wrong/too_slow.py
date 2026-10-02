from itertools import combinations


class Solution:
    # Mistake: tries every way to choose n of the 2n players.
    def smallestGap(self, skills):
        n = len(skills) // 2
        total = sum(skills)
        return min(abs(total - 2 * sum(c)) for c in combinations(skills, n))
