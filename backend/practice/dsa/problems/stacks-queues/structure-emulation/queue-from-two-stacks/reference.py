class TwoStackQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def _turn(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        self._turn()
        return self.outbox.pop()

    def peek(self):
        self._turn()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox
