from bisect import bisect_left


class Solution:
    def smallestGap(self, skills):
        n = len(skills) // 2

        def diffs(xs):
            by = [[] for _ in range(len(xs) + 1)]
            m = len(xs)
            for mask in range(1 << m):
                k, d = 0, 0
                for i in range(m):
                    if mask >> i & 1:
                        k += 1
                        d += xs[i]
                    else:
                        d -= xs[i]
                by[k].append(d)
            return by

        L, R = diffs(skills[:n]), diffs(skills[n:])
        best = None
        for k in range(n + 1):
            right = sorted(R[n - k])
            for d in L[k]:
                j = bisect_left(right, -d)
                for t in (j - 1, j):
                    if 0 <= t < len(right):
                        v = abs(d + right[t])
                        if best is None or v < best:
                            best = v
        return best
