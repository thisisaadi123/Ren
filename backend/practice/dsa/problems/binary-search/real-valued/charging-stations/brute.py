class Solution:
    def smallestMaxGap(self, stations, extra):
        # Greedy: always split the gap whose pieces are currently the longest.
        heap = [(-(b - a), b - a, 1) for a, b in zip(stations, stations[1:])]
        heapq.heapify(heap)
        for _ in range(extra):
            _, g, parts = heapq.heappop(heap)
            parts += 1
            heapq.heappush(heap, (-g / parts, g, parts))
        return -heap[0][0]
