import random
class Solution:
    def middleReading(self, readings):
        a = readings[:]
        k = len(a) // 2
        rng = random.Random(3)
        lo, hi = 0, len(a) - 1
        while True:
            p = a[rng.randint(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < p:
                    a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
                elif a[i] > p:
                    a[i], a[gt] = a[gt], a[i]; gt -= 1
                else:
                    i += 1
            if k < lt:
                hi = lt - 1
            elif k > gt:
                lo = gt + 1
            else:
                return p
