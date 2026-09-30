class Solution:
    # Mistake: assumes everyone can share.
    def fewestBoats(self, weights, limit):
        return (len(weights) + 1) // 2
