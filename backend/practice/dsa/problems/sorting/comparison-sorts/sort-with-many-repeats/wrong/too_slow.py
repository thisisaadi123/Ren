class Solution:
    # Two-way quick sort with the first element as pivot: quadratic on repeats.
    def sortReadings(self, readings):
        a = readings[:]
        stack = [(0, len(a) - 1)]
        while stack:
            lo, hi = stack.pop()
            if lo >= hi:
                continue
            p, i = a[hi], lo
            for j in range(lo, hi):
                if a[j] <= p:
                    a[i], a[j] = a[j], a[i]; i += 1
            a[i], a[hi] = a[hi], a[i]
            stack.append((lo, i - 1))
            stack.append((i + 1, hi))
        return a
