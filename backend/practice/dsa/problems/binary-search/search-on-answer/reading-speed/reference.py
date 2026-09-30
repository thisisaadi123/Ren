class Solution:
    def minReadingSpeed(self, books, hours):
        lo, hi = 1, max(books)
        while lo < hi:
            mid = (lo + hi) // 2
            if sum((p + mid - 1) // mid for p in books) <= hours:
                hi = mid
            else:
                lo = mid + 1
        return lo
