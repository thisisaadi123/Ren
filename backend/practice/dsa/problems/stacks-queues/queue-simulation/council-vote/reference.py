from collections import deque


class Solution:
    def councilWinner(self, council):
        n = len(council)
        larks = deque(i for i, c in enumerate(council) if c == "L")
        owls = deque(i for i, c in enumerate(council) if c == "O")
        while larks and owls:
            a, b = larks.popleft(), owls.popleft()
            if a < b:
                larks.append(a + n)
            else:
                owls.append(b + n)
        return "Larks" if larks else "Owls"
