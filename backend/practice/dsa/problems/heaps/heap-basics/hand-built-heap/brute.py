class TaskHeap:
    def __init__(self, items):
        self.a = sorted(items)

    def push(self, x):
        self.a.append(x)
        self.a.sort()

    def pop(self):
        return self.a.pop(0) if self.a else -1

    def peek(self):
        return self.a[0] if self.a else -1

    def size(self):
        return len(self.a)
