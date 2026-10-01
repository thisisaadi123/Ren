from collections import deque


class Solution:
    def longestSteady(self, readings, limit):
        hi, lo = deque(), deque()
        left = best = 0
        for i, v in enumerate(readings):
            while hi and readings[hi[-1]] <= v:
                hi.pop()
            hi.append(i)
            while lo and readings[lo[-1]] >= v:
                lo.pop()
            lo.append(i)
            while readings[hi[0]] - readings[lo[0]] > limit:
                left += 1
                if hi[0] < left:
                    hi.popleft()
                if lo[0] < left:
                    lo.popleft()
            best = max(best, i - left + 1)
        return best
