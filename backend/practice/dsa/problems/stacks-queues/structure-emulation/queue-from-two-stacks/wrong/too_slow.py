class TwoStackQueue:
    # Mistake: pours every item across and back on each pop: O(n) per call.
    def __init__(self):
        self.a = []

    def push(self, x):
        self.a.append(x)

    def pop(self):
        b = []
        while self.a:
            b.append(self.a.pop())
        x = b.pop()
        while b:
            self.a.append(b.pop())
        return x

    def peek(self):
        b = []
        while self.a:
            b.append(self.a.pop())
        x = b[-1]
        while b:
            self.a.append(b.pop())
        return x

    def empty(self):
        return not self.a
