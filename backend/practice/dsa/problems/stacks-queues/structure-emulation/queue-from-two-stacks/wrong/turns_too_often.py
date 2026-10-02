class TwoStackQueue:
    # Mistake: moves the inbox over even when the outbox still has older items.
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def _turn(self):
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
