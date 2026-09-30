class Solution:
    # Mistake: forgets the wrap-around, so "az" and "ba" look like different families.
    def countShiftFamilies(self, words):
        return len({tuple(ord(b) - ord(a) for a, b in zip(w, w[1:])) + (len(w),) for w in words})
