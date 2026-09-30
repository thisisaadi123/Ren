class Solution:
    # Mistake: lets the same weight be used more than once.
    def hasTriple(self, weights, target):
        s = set(weights)
        return any(target - a - b in s for a in weights for b in weights)
