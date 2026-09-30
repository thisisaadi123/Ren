class Solution:
    # Mistake: adds the raw radii in the #-padded string, double counting.
    def palindromeCensus(self, s):
        t = "^#" + "#".join(s) + "#$"
        n = len(t)
        p = [0] * n
        center = right = 0
        for i in range(1, n - 1):
            if i < right:
                p[i] = min(right - i, p[2 * center - i])
            while t[i + p[i] + 1] == t[i - p[i] - 1]:
                p[i] += 1
            if i + p[i] > right:
                center, right = i, i + p[i]
        return sum(p)
