class Solution:
    def countSameShape(self, words, pattern):
        def same(a, b):
            if len(a) != len(b):
                return False
            fwd, back = {}, {}
            for x, y in zip(a, b):
                if fwd.setdefault(x, y) != y or back.setdefault(y, x) != x:
                    return False
            return True
        return sum(same(w, pattern) for w in words)
