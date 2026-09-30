class Solution:
    # Mistake: counts every matched pair in the whole string, even pairs separated by a stray bracket.
    def longestBalanced(self, s):
        d = pairs = 0
        for c in s:
            if c == "(":
                d += 1
            elif d:
                d -= 1
                pairs += 1
        return 2 * pairs
