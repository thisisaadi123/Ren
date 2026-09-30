class Solution:
    def countSameShape(self, words, pattern):
        def shape(w):
            first = {}
            return tuple(first.setdefault(c, len(first)) for c in w)
        target = shape(pattern)
        return sum(shape(w) == target for w in words)
