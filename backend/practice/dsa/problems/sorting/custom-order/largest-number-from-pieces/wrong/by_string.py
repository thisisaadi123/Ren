class Solution:
    # Mistake: plain string order puts 3 after 30 wrongly.
    def largestNumber(self, pieces):
        out = "".join(sorted(map(str, pieces), reverse=True))
        return "0" if out[0] == "0" else out
