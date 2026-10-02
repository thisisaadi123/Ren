class TwoStackQueue:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[0]

    def empty(self):
        return not self.items
