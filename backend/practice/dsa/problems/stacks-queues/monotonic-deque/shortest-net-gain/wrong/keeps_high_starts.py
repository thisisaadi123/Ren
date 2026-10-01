from collections import deque


class Solution:
    # Mistake: never drops later prefixes that are not lower, so some good starts are hidden behind worse ones.
    def shortestNetGain(self, changes, target):
        n = len(changes)
        prefix = [0] * (n + 1)
        for i, v in enumerate(changes):
            prefix[i + 1] = prefix[i] + v
        best = n + 1
        dq = deque()
        for j in range(n + 1):
            while dq and prefix[j] - prefix[dq[0]] >= target:
                best = min(best, j - dq.popleft())
            dq.append(j)
        return best if best <= n else -1
