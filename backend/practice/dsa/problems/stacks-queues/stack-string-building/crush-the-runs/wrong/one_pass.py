class Solution:
    # Mistake: crushes runs once, left to right, but never checks the new runs that form.
    def crushRuns(self, s, k):
        out = []
        i = 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            out.append(s[i] * ((j - i) % k))
            i = j
        return "".join(out)
