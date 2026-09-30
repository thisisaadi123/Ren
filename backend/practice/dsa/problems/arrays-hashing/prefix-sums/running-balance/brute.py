class Solution:
    def runningBalance(self, changes):
        return [sum(changes[: i + 1]) for i in range(len(changes))]
