class Solution:
    def zeroTriples(self, values):
        a = sorted(values)
        n = len(a)
        out = []
        for i in range(n - 2):
            if i and a[i] == a[i - 1]:
                continue
            if a[i] > 0:
                break
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
                    while j < k and a[j] == a[j - 1]:
                        j += 1
                    k -= 1
        return out
