class Solution:
    def findRepeat(self, tickets):
        for v in range(1, len(tickets)):
            if tickets.count(v) > 1:
                return v
        return -1
