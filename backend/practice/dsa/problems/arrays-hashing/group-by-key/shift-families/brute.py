class Solution:
    def countShiftFamilies(self, words):
        def shift(w, k):
            return "".join(chr((ord(c) - 97 + k) % 26 + 97) for c in w)
        reps = []
        for w in words:
            if not any(len(r) == len(w) and any(shift(r, k) == w for k in range(26)) for r in reps):
                reps.append(w)
        return len(reps)
