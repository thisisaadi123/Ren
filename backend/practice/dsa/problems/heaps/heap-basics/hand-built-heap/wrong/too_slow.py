class TaskHeap:
    # Mistake: scans the whole list for the smallest value on every pop.
    def __init__(self, items):
        self.a = list(items)

    def push(self, x):
        self.a.append(x)

    def pop(self):
        if not self.a:
            return -1
        i = self.a.index(min(self.a))
        self.a[i] = self.a[-1]
        return self.a.pop() if i == len(self.a) - 1 else self._swap_pop(i)

    def _swap_pop(self, i):
        v = min(self.a[i], self.a[-1])
        self.a.pop()
        return v

    def peek(self):
        return min(self.a) if self.a else -1

    def size(self):
        return len(self.a)
