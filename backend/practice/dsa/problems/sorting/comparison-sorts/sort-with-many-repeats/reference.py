import random
class Solution:
    def sortReadings(self, readings):
        a = readings[:]
        rng = random.Random(7)
        stack = [(0, len(a) - 1)]
        while stack:
            lo, hi = stack.pop()
            if lo >= hi:
                continue
            p = a[rng.randint(lo, hi)]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < p:
                    a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
                elif a[i] > p:
                    a[i], a[gt] = a[gt], a[i]; gt -= 1
                else:
                    i += 1
            stack.append((lo, lt - 1))
            stack.append((gt + 1, hi))
        return a
