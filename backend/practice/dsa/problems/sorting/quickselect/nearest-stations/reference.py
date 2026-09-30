import random
class Solution:
    def nearestStations(self, stations, k):
        key = lambda p: (p[0] * p[0] + p[1] * p[1], p[0], p[1])
        a = [key(p) for p in stations]
        rng = random.Random(11)
        lo, hi = 0, len(a) - 1
        target = k - 1
        while lo < hi:
            p = a[rng.randint(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < p:
                    a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
                elif a[i] > p:
                    a[i], a[gt] = a[gt], a[i]; gt -= 1
                else:
                    i += 1
            if target < lt:
                hi = lt - 1
            elif target > gt:
                lo = gt + 1
            else:
                break
        return [[x, y] for _, x, y in sorted(a[:k])]
