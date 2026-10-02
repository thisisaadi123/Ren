class Solution:
    # Mistake: stops after checking that both roots exist and match.
    def twins(self, a, b):
        if not a or not b:
            return a is b
        return a.val == b.val
