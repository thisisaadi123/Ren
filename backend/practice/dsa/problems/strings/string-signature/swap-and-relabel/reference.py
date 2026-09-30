class Solution:
    def canReshape(self, a, b):
        if len(a) != len(b):
            return False
        ca, cb = [0] * 26, [0] * 26
        for c in a:
            ca[ord(c) - 97] += 1
        for c in b:
            cb[ord(c) - 97] += 1
        for x, y in zip(ca, cb):
            if (x > 0) != (y > 0):
                return False
        return sorted(ca) == sorted(cb)
