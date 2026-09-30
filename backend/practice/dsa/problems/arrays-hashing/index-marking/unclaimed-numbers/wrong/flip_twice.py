class Solution:
    # Mistake: flips the sign every time, so a value seen twice looks unseen again.
    def findUnclaimed(self, tickets):
        for v in tickets:
            i = abs(v) - 1
            tickets[i] = -tickets[i]
        return [i + 1 for i, v in enumerate(tickets) if v > 0]
