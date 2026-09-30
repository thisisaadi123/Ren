class Solution:
    # Mistake: looks for two weights, not three.
    def hasTriple(self, weights, target):
        seen = set()
        for x in weights:
            if target - x in seen:
                return True
            seen.add(x)
        return False
