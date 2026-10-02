class TaskHeap:
    def __init__(self, items):
        self.a = list(items)
        for i in range(len(self.a) // 2 - 1, -1, -1):
            self._down(i)

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
        a = self.a
        if not a:
            return -1
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last
            self._down(0)
        return top

    def peek(self):
        return self.a[0] if self.a else -1

    def size(self):
        return len(self.a)
