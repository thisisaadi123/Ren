class Solution:
    # Mistake: returns one past the last match.
    def deliveryRange(self, times, target):
        import bisect
        a = bisect.bisect_left(times, target)
        if a == len(times) or times[a] != target:
            return [-1, -1]
        return [a, bisect.bisect_right(times, target)]
