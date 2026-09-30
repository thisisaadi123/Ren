class Solution:
    # Mistake: computes letters as 3 per key, so 7 has no 's', and 8 and 9 are shifted.
    def keypadSpellings(self, digits):
        if not digits:
            return []
        out = [""]
        for d in digits:
            base = 3 * (int(d) - 2)
            out = [s + chr(97 + base + j) for s in out for j in range(3)]
        return out
