from functools import lru_cache


class Solution:
    def minDailyLimit(self, pages, days):
        # Try every way to cut the queue into at most `days` consecutive groups;
        # the answer is the smallest possible biggest group. No binary search, no greedy.
        n = len(pages)

        @lru_cache(maxsize=None)
        def best(start, groups_left):
            if start == n:
                return 0
            if groups_left == 0:
                return float("inf")
            result = float("inf")
            total = 0
            for end in range(start, n):
                total += pages[end]
                result = min(result, max(total, best(end + 1, groups_left - 1)))
            return result

        return best(0, days)
