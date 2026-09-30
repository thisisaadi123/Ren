class Solution:
    # Mistake: values the string by its deepest box alone, ignoring boxes side by side.
    def boxValue(self, s):
        d = best = 0
        for c in s:
            d += 1 if c == "(" else -1
            best = max(best, d)
        return pow(2, best - 1, 10**9 + 7)
