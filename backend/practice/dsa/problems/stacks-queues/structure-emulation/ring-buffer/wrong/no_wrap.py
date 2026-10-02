class RingBuffer:
    # Mistake: uses head and tail indexes that never wrap, so space freed at the front is never reused.
    def __init__(self, k):
        self.buf = [0] * k
        self.k = k
        self.head = 0
        self.tail = 0

    def enqueue(self, x):
        if self.tail == self.k:
            return False
        self.buf[self.tail] = x
        self.tail += 1
        return True

    def dequeue(self):
        if self.head == self.tail:
            return False
        self.head += 1
        return True

    def front(self):
        return self.buf[self.head] if self.head < self.tail else -1

    def rear(self):
        return self.buf[self.tail - 1] if self.head < self.tail else -1

    def isEmpty(self):
        return self.head == self.tail

    def isFull(self):
        return self.tail == self.k
