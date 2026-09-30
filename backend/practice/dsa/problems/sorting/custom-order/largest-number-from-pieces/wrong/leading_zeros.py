import functools
class Solution:
    # Mistake: keeps "00" instead of "0".
    def largestNumber(self, pieces):
        s = [str(p) for p in pieces]
        s.sort(key=functools.cmp_to_key(lambda a, b: (a + b < b + a) - (a + b > b + a)))
        return "".join(s)
