class Solution:
    def zeroTriples(self, values):
        n = len(values)
        found = set()
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if values[i] + values[j] + values[k] == 0:
                        found.add(tuple(sorted((values[i], values[j], values[k]))))
        return [list(t) for t in sorted(found)]
