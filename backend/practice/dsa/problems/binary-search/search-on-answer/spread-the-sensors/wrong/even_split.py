class Solution:
    # Mistake: assumes the spots allow a perfectly even split.
    def widestSpacing(self, spots, sensors):
        return (max(spots) - min(spots)) // (sensors - 1)
