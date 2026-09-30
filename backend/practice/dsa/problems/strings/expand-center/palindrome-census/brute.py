class Solution:
    def palindromeCensus(self, s):
        n = len(s)
        return sum(1 for i in range(n) for j in range(i + 1, n + 1) if s[i:j] == s[i:j][::-1])
