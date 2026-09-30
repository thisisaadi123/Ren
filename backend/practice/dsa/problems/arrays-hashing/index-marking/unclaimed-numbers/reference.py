class Solution:
    def findUnclaimed(self, tickets):
        for v in tickets:
            i = abs(v) - 1
            if tickets[i] > 0:
                tickets[i] = -tickets[i]
        return [i + 1 for i, v in enumerate(tickets) if v > 0]
