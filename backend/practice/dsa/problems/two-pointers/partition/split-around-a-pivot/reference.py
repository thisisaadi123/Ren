class Solution:
    def splitAround(self, values, pivot):
        less = sum(1 for x in values if x < pivot)
        equal = sum(1 for x in values if x == pivot)
        out = [0] * len(values)
        a, b, c = 0, less, less + equal
        for x in values:
            if x < pivot:
                out[a] = x; a += 1
            elif x == pivot:
                out[b] = x; b += 1
            else:
                out[c] = x; c += 1
        return out
