class Solution:
    def hasDuplicate(self, badges):
        n = len(badges)
        return any(badges[i] == badges[j] for i in range(n) for j in range(i + 1, n))
