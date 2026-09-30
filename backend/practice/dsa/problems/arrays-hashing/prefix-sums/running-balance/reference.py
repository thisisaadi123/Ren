class Solution:
    def runningBalance(self, changes):
        out, total = [], 0
        for c in changes:
            total += c
            out.append(total)
        return out
