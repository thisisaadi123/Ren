class Solution:
    def minDailyLimit(self, pages, days):
        def days_needed(limit):
            used, load = 1, 0
            for p in pages:
                if load + p > limit:
                    used += 1
                    load = 0
                load += p
            return used

        # The answer is at least the biggest job and at most everything in one day.
        lo, hi = max(pages), sum(pages)
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                hi = mid
            else:
                lo = mid + 1
        return lo
