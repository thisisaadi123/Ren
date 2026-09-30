class Solution:
    def deliveryRange(self, times, target):
        def first_at_least(x):
            lo, hi = 0, len(times)
            while lo < hi:
                mid = (lo + hi) // 2
                if times[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        a = first_at_least(target)
        if a == len(times) or times[a] != target:
            return [-1, -1]
        return [a, first_at_least(target + 1) - 1]
