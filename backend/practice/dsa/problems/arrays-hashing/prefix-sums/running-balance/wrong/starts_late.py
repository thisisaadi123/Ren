class Solution:
    # Mistake: reports the balance at the start of each day instead of the end.
    def runningBalance(self, changes):
        out, total = [], 0
        for c in changes:
            out.append(total)
            total += c
        return out
