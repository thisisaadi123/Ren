class Solution:
    # Mistake: re-sorts everything after each reading.
    def runningMiddle(self, readings):
        out = []
        for m in range(1, len(readings) + 1):
            out.append(sorted(readings[:m])[(m + 1) // 2 - 1])
        return out
