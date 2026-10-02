import heapq


class Solution:
    # Mistake: reports the upper middle when the count is even.
    def runningMiddle(self, readings):
        low, high, out = [], [], []
        for x in readings:
            heapq.heappush(high, x)
            heapq.heappush(low, -heapq.heappop(high))
            if len(low) > len(high):
                heapq.heappush(high, -heapq.heappop(low))
            out.append(high[0])
        return out
