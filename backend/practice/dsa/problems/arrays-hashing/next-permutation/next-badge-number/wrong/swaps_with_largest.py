class Solution:
    # Mistake: swaps with the first digit after i, which is the LARGEST bigger digit, not the smallest.
    def nextBadge(self, code):
        d = list(code)
        i = len(d) - 2
        while i >= 0 and d[i] >= d[i + 1]:
            i -= 1
        if i < 0:
            return ""
        d[i], d[i + 1] = d[i + 1], d[i]
        d[i + 1:] = reversed(d[i + 1:])
        return "".join(d)
