class Solution:
    # Mistake: grows a window from every start: O(n^2).
    def shortestSampler(self, jars):
        d = len(set(jars))
        n = len(jars)
        best = n
        for i in range(n):
            seen = set()
            for j in range(i, n):
                seen.add(jars[j])
                if len(seen) == d:
                    best = min(best, j - i + 1)
                    break
        return best
