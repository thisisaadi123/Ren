class Solution:
    # Mistake: only checks that each kind has as many closers as openers, never the order.
    def isSealed(self, s):
        return all(s.count(a) == s.count(b) for a, b in ("()", "[]", "{}"))
