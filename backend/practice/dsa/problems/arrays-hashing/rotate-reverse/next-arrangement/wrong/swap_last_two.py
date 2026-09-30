class Solution:
    # Mistake: only swaps the last two values.
    def nextArrangement(self, values):
        a = values[:]
        if len(a) > 1:
            a[-1], a[-2] = a[-2], a[-1]
        return a
