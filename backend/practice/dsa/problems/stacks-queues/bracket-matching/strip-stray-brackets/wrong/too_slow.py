class Solution:
    # Mistake: removes one stray bracket at a time and rescans the whole string: O(n²).
    def stripStray(self, s):
        while True:
            d, bad = 0, -1
            for i, c in enumerate(s):
                if c == "(":
                    d += 1
                elif c == ")":
                    d -= 1
                    if d < 0:
                        bad = i
                        break
            if bad < 0:
                break
            s = s[:bad] + s[bad + 1:]
        while True:
            d, last = 0, -1
            for i, c in enumerate(s):
                if c == "(":
                    d += 1
                    last = i
                elif c == ")":
                    d -= 1
            if d == 0:
                return s
            s = s[:last] + s[last + 1:]
