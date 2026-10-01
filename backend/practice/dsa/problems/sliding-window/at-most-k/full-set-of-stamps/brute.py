class Solution:
    def countFullSets(self, s):
        n = len(s)
        return sum(1 for i in range(n) for j in range(i + 3, n + 1) if set(s[i:j]) == {"a", "b", "c"})
