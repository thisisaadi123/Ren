class Solution:
    # Mistake: only checks pattern -> word, so "ab" wrongly matches "cc".
    def countSameShape(self, words, pattern):
        def ok(w):
            if len(w) != len(pattern):
                return False
            m = {}
            return all(m.setdefault(p, c) == c for p, c in zip(pattern, w))
        return sum(ok(w) for w in words)
