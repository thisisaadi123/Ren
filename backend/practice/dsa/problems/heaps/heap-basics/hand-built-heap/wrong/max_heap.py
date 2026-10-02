import heapq


class TaskHeap:
    # Mistake: returns the largest value instead of the smallest.
    def __init__(self, items):
        self.a = [-v for v in items]
        heapq.heapify(self.a)

    def push(self, x):
        heapq.heappush(self.a, -x)

    def pop(self):
        return -heapq.heappop(self.a) if self.a else -1

    def peek(self):
        return -self.a[0] if self.a else -1

    def size(self):
        return len(self.a)
