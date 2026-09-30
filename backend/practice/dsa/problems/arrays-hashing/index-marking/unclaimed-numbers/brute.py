class Solution:
    def findUnclaimed(self, tickets):
        return [x for x in range(1, len(tickets) + 1) if x not in tickets]
