class RingBuffer:
    # Mistake: accepts one item more than k.
    def __init__(self, k):
        self.items = []
        self.k = k

    def enqueue(self, x):
        if len(self.items) > self.k:
            return False
        self.items.append(x)
        return True

    def dequeue(self):
        if not self.items:
            return False
        self.items.pop(0)
        return True

    def front(self):
        return self.items[0] if self.items else -1

    def rear(self):
        return self.items[-1] if self.items else -1

    def isEmpty(self):
        return not self.items

    def isFull(self):
        return len(self.items) >= self.k
