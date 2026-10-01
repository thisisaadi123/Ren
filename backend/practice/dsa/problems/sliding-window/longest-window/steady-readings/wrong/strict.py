class Solution:
    # Mistake: requires the spread to be strictly below limit.
    def longestSteady(self, readings, limit):
        from collections import deque
        hi, lo = deque(), deque()
        left = best = 0
        for i, v in enumerate(readings):
            while hi and readings[hi[-1]] <= v:
                hi.pop()
            hi.append(i)
            while lo and readings[lo[-1]] >= v:
                lo.pop()
            lo.append(i)
            while left <= i and readings[hi[0]] - readings[lo[0]] >= limit:
                left += 1
                if hi and hi[0] < left:
                    hi.popleft()
                if lo and lo[0] < left:
                    lo.popleft()
                if not hi or not lo:
                    break
            best = max(best, i - left + 1)
        return best
