class Solution:
    # Mistake: starts the search at the average day load instead of the biggest
    # job, and the greedy count doesn't notice a job bigger than the limit.
    def minDailyLimit(self, pages, days):
        def days_needed(limit):
            used, load = 1, 0
            for p in pages:
                if load + p > limit:
                    used += 1
                    load = 0
                load += p
            return used

        lo, hi = max(1, sum(pages) // days), sum(pages)
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                hi = mid
            else:
                lo = mid + 1
        return lo
