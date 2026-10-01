from collections import deque


class Solution:
    # Mistake: lets the waiter take the BOTTOM plate, as if the plates formed a queue.
    def couldHappen(self, washed, served):
        q = deque()
        j = 0
        for plate in washed:
            q.append(plate)
            while q and (q[-1] == served[j] or q[0] == served[j]):
                if q[-1] == served[j]:
                    q.pop()
                else:
                    q.popleft()
                j += 1
        return j == len(served)
