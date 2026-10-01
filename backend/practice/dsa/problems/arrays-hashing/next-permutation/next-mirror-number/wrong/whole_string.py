class Solution:
    # Mistake: takes the next arrangement of the whole string, which is usually not a mirror number.
    def nextMirror(self, code):
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
        d[i + 1:] = reversed(d[i + 1:])
        return "".join(d)
