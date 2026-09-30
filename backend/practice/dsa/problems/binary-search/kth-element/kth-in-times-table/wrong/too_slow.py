class Solution:
    # Pops the k smallest values from a heap: correct, but O(k log rows).
    def kthInTable(self, rows, cols, k):
        heap = [(i, i, 1) for i in range(1, rows + 1)]
        heapq.heapify(heap)
        for _ in range(k):
            v, i, j = heapq.heappop(heap)
            if j < cols:
                heapq.heappush(heap, (i * (j + 1), i, j + 1))
        return v
