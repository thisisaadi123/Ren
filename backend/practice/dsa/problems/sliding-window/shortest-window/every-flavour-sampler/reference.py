class Solution:
    def shortestSampler(self, jars):
        d = len(set(jars))
        count = {}
        left = 0
        best = len(jars)
        for i, f in enumerate(jars):
            count[f] = count.get(f, 0) + 1
            while len(count) == d:
                best = min(best, i - left + 1)
                g = jars[left]
                count[g] -= 1
                if count[g] == 0:
                    del count[g]
                left += 1
        return best
