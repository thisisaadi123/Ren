class Solution:
    # Mistake: sorts and deals players alternately to the two teams.
    def smallestGap(self, skills):
        xs = sorted(skills)
        a = sum(xs[0::4]) + sum(xs[3::4])
        b = sum(xs) - a
        return abs(a - b)
