class Solution:
    # Mistake: starts the search one above the biggest job, so it can never
    # answer max(pages), e.g. when there are as many days as jobs.
    def minDailyLimit(self, pages, days):
        def days_needed(limit):
            used, load = 1, 0
            for p in pages:
                if load + p > limit:
                    used += 1
                    load = 0
                load += p
            return used

        lo, hi = max(pages) + 1, sum(pages) + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                hi = mid
            else:
                lo = mid + 1
        return lo
