class Solution:
    def closestTriple(self, values, target):
        a = sorted(values)
        n = len(a)
        best = a[0] + a[1] + a[2]
        gap = abs(best - target)
        for i in range(n - 2):
            ai = a[i]
            j, k = i + 1, n - 1
            while j < k:
                s = ai + a[j] + a[k]
                d = s - target
                if d < 0:
                    if -d < gap or (-d == gap and s < best):
                        best, gap = s, -d
                    j += 1
                elif d > 0:
                    if d < gap or (d == gap and s < best):
                        best, gap = s, d
                    k -= 1
                else:
                    return s
        return best
