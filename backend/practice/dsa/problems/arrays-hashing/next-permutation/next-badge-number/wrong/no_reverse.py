class Solution:
    # Mistake: leaves the tail in descending order after the swap.
    def nextBadge(self, code):
        d = list(code)
        i = len(d) - 2
        while i >= 0 and d[i] >= d[i + 1]:
            i -= 1
        if i < 0:
            return ""
        j = len(d) - 1
        while d[j] <= d[i]:
            j -= 1
        d[i], d[j] = d[j], d[i]
        return "".join(d)
