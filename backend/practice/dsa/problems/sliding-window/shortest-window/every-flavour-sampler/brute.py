class Solution:
    def shortestSampler(self, jars):
        d = len(set(jars))
        n = len(jars)
        return min(j - i + 1 for i in range(n) for j in range(i, n) if len(set(jars[i:j + 1])) == d)
