import heapq


class Solution:
    def runningMiddle(self, readings):
        low, high, out = [], [], []
        for x in readings:
            heapq.heappush(low, -x)
            heapq.heappush(high, -heapq.heappop(low))
            if len(high) > len(low):
                heapq.heappush(low, -heapq.heappop(high))
            out.append(-low[0])
        return out
