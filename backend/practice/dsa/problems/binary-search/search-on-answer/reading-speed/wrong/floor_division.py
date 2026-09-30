class Solution:
    # Mistake: rounds hours down, forgetting that a partial hour still costs an hour.
    def minReadingSpeed(self, books, hours):
        lo, hi = 1, max(books)
        while lo < hi:
            mid = (lo + hi) // 2
            if sum(max(1, p // mid) for p in books) <= hours:
                hi = mid
            else:
                lo = mid + 1
        return lo
