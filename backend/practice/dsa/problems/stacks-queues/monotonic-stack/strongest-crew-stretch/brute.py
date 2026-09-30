class Solution:
    def strongestCrew(self, strength):
        n = len(strength)
        return max(min(strength[i:j + 1]) * sum(strength[i:j + 1]) for i in range(n) for j in range(i, n))
