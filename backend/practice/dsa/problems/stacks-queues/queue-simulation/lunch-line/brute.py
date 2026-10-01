from collections import deque


class Solution:
    def hungryStudents(self, prefers, trays):
        q = deque(prefers)
        top = 0
        misses = 0
        while q and misses < len(q):
            s = q.popleft()
            if s == trays[top]:
                top += 1
                misses = 0
            else:
                q.append(s)
                misses += 1
        return len(q)
