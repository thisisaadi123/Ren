class Solution:
    def oneSlip(self, s):
        options = [s] + [s[:k] + s[k + 1:] for k in range(len(s))]
        return any(t == t[::-1] for t in options)
