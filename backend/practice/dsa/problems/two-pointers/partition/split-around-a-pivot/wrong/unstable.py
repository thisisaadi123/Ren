class Solution:
    # Mistake: a Dutch-flag pass is fast but scrambles the order inside groups.
    def splitAround(self, values, pivot):
        a = values[:]
        lo, mid, hi = 0, 0, len(a) - 1
        while mid <= hi:
            if a[mid] < pivot:
                a[lo], a[mid] = a[mid], a[lo]; lo += 1; mid += 1
            elif a[mid] > pivot:
                a[mid], a[hi] = a[hi], a[mid]; hi -= 1
            else:
                mid += 1
        return a
