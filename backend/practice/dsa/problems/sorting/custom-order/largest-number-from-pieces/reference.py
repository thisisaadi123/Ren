import functools
class Solution:
    def largestNumber(self, pieces):
        s = [str(p) for p in pieces]
        s.sort(key=functools.cmp_to_key(lambda a, b: (a + b < b + a) - (a + b > b + a)))
        out = "".join(s)
        return "0" if out[0] == "0" else out
