from collections import deque


class Solution:
    def bestScore(self, stones, k):
        n = len(stones)
        best = [0] * n
        best[0] = stones[0]
        dq = deque([0])
        for i in range(1, n):
            if dq[0] < i - k:
                dq.popleft()
            best[i] = stones[i] + best[dq[0]]
            while dq and best[dq[-1]] <= best[i]:
                dq.pop()
            dq.append(i)
        return best[-1]
