class Solution:
    # Mistake: a three-way pass that only separates 1, 2 and the rest.
    def sortKColours(self, balls, k):
        a = balls[:]
        lo, mid, hi = 0, 0, len(a) - 1
        while mid <= hi:
            if a[mid] == 1:
                a[lo], a[mid] = a[mid], a[lo]; lo += 1; mid += 1
            elif a[mid] > 2:
                a[mid], a[hi] = a[hi], a[mid]; hi -= 1
            else:
                mid += 1
        return a
