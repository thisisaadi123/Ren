from collections import deque


class Solution:
    # Mistake: survivors don't get another turn, so only the first round counts.
    def councilWinner(self, council):
        larks = deque(i for i, c in enumerate(council) if c == "L")
        owls = deque(i for i, c in enumerate(council) if c == "O")
        while larks and owls:
            a, b = larks.popleft(), owls.popleft()
            if a < b:
                larks.append(a)
                if len(larks) and len(owls) and larks[0] == a:
                    break
            else:
                owls.append(b)
                if len(larks) and len(owls) and owls[0] == b:
                    break
        return "Larks" if len(larks) >= len(owls) else "Owls"
