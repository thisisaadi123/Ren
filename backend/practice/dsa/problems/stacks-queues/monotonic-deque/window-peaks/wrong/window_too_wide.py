from collections import deque


class Solution:
    # Mistake: evicts the front one step late, so the window holds k + 1 readings.
    def windowPeaks(self, temps, k):
        dq = deque()
        out = []
        for i, v in enumerate(temps):
            while dq and temps[dq[-1]] <= v:
                dq.pop()
            dq.append(i)
            if dq[0] < i - k:
                dq.popleft()
            if i >= k - 1:
                out.append(temps[dq[0]])
        return out
