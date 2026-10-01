class Solution:
    # Mistake: on a third flavour keeps only the single previous tub, not its whole run.
    def mostScoops(self, flavours):
        left = best = 0
        for i in range(len(flavours)):
            if len(set(flavours[left:i + 1])) > 2:
                left = i - 1
            best = max(best, i - left + 1)
        return best
