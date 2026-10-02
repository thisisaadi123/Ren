class TwoStackQueue:
    # Mistake: pops the newest item, like a stack.
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def empty(self):
        return not self.items
