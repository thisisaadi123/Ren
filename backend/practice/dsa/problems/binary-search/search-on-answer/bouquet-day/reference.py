class Solution:
    def earliestBouquetDay(self, bloom, bouquets, size):
        if bouquets * size > len(bloom):
            return -1

        def can(day):
            made = run = 0
            for b in bloom:
                run = run + 1 if b <= day else 0
                if run == size:
                    made += 1
                    run = 0
            return made >= bouquets

        lo, hi = min(bloom), max(bloom)
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
