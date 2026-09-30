class Solution:
    def countShiftFamilies(self, words):
        return len({tuple((ord(b) - ord(a)) % 26 for a, b in zip(w, w[1:])) + (len(w),) for w in words})
