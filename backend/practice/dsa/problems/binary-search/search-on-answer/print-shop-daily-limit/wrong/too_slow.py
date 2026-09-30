class Solution:
    # Correct but too slow: tries every limit upward instead of binary searching.
    def minDailyLimit(self, pages, days):
        limit = max(pages)
        while True:
            used, load = 1, 0
            for p in pages:
                if load + p > limit:
                    used += 1
                    load = 0
                load += p
            if used <= days:
                return limit
            limit += 1
