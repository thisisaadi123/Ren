class Solution:
    # Mistake: sorts the pieces by numeric value.
    def largestNumber(self, pieces):
        out = "".join(str(p) for p in sorted(pieces, reverse=True))
        return "0" if out[0] == "0" else out
