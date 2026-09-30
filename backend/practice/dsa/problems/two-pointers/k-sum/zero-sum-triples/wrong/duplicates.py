class Solution:
    # Mistake: doesn't skip repeated values, so the same triple appears twice.
    def zeroTriples(self, values):
        a = sorted(values)
        n = len(a)
        out = []
        for i in range(n - 2):
            j, k = i + 1, n - 1
            while j < k:
                s = a[i] + a[j] + a[k]
                if s < 0:
                    j += 1
                elif s > 0:
                    k -= 1
                else:
                    out.append([a[i], a[j], a[k]])
                    j += 1
                    k -= 1
        return out
