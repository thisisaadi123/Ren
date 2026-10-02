class TaskHeap:
    # Mistake: keeps the starting items in their given order instead of heapifying them.
    def __init__(self, items):
        self.a = list(items)

    def _up(self, i):
        a = self.a
        while i and a[i] < a[(i - 1) // 2]:
            p = (i - 1) // 2
            a[i], a[p] = a[p], a[i]
            i = p

    def _down(self, i):
        a, n = self.a, len(self.a)
        while True:
            m, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and a[l] < a[m]:
                m = l
            if r < n and a[r] < a[m]:
                m = r
            if m == i:
                return
            a[i], a[m] = a[m], a[i]
            i = m

    def push(self, x):
        self.a.append(x)
        self._up(len(self.a) - 1)

    def pop(self):
        if not self.a:
            return -1
        top, last = self.a[0], self.a.pop()
        if self.a:
            self.a[0] = last
            self._down(0)
        return top

    def peek(self):
        return self.a[0] if self.a else -1

    def size(self):
        return len(self.a)
