class Solution:
    # Mistake: uses the absolute gap, so "ab" and "ba" look like the same family.
    def countShiftFamilies(self, words):
        return len({tuple(abs(ord(b) - ord(a)) for a, b in zip(w, w[1:])) for w in words})
