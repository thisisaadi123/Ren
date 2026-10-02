import heapq


class Solution:
    # Mistake: drops each reading into a half by comparing with the middle, but never rebalances.
    def runningMiddle(self, readings):
        low, high, out = [], [], []
        for x in readings:
            if not low or x <= -low[0]:
                heapq.heappush(low, -x)
            else:
                heapq.heappush(high, x)
            out.append(-low[0])
        return out
