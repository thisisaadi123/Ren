class Solution:
    # Mistake: throws the whole window away at a repeat and starts again from the repeated letter.
    def longestFresh(self, s):
        seen = set()
        best = 0
        for c in s:
            if c in seen:
                seen = set()
            seen.add(c)
            best = max(best, len(seen))
        return best
