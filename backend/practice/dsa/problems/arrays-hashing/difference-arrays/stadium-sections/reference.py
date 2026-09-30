class Solution:
    def sectionCounts(self, n, groups):
        diff = [0] * (n + 1)
        for l, r, people in groups:
            diff[l] += people
            diff[r + 1] -= people
        out, running = [], 0
        for i in range(n):
            running += diff[i]
            out.append(running)
        return out
