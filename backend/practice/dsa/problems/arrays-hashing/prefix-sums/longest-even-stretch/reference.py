class Solution:
    def longestEvenStretch(self, bits):
        first = {0: -1}
        best = total = 0
        for i, b in enumerate(bits):
            total += 1 if b else -1
            if total in first:
                best = max(best, i - first[total])
            else:
                first[total] = i
        return best
