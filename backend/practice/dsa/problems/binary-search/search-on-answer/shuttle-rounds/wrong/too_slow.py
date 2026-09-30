class Solution:
    # Simulates each finished round with a heap: correct, but O(totalRounds log n).
    def minTimeForRounds(self, roundTime, totalRounds):
        heap = [(t, t) for t in roundTime]
        heapq.heapify(heap)
        done = 0
        while True:
            finish, t = heapq.heappop(heap)
            done += 1
            if done == totalRounds:
                return finish
            heapq.heappush(heap, (finish + t, t))
