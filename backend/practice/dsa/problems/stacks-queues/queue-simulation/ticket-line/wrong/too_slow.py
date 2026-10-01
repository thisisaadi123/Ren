from collections import deque


class Solution:
    # Mistake: simulates every second: O(total tickets).
    def secondsToFinish(self, wants, k):
        line = deque((w, i) for i, w in enumerate(wants))
        t = 0
        while True:
            w, i = line.popleft()
            t += 1
            if w == 1:
                if i == k:
                    return t
            else:
                line.append((w - 1, i))
