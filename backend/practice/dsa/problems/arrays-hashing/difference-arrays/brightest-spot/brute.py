class Solution:
    def brightestSpot(self, lamps):
        # The answer is always the left end of some lamp's light.
        candidates = sorted(p - r for p, r in lamps)
        return max(candidates, key=lambda x: (sum(p - r <= x <= p + r for p, r in lamps), -x))
