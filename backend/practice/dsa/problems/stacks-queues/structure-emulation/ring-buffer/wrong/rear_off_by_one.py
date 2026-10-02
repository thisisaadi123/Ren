class RingBuffer:
    # Mistake: reads rear() one slot too far, at (head + size) % k.
    def __init__(self, k):
        self.buf = [0] * k
        self.k = k
        self.head = 0
        self.size = 0

    def enqueue(self, x):
        if self.size == self.k:
            return False
        self.buf[(self.head + self.size) % self.k] = x
        self.size += 1
        return True

    def dequeue(self):
        if self.size == 0:
            return False
        self.head = (self.head + 1) % self.k
        self.size -= 1
        return True

    def front(self):
        return self.buf[self.head] if self.size else -1

    def rear(self):
        return self.buf[(self.head + self.size) % self.k] if self.size else -1

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k
