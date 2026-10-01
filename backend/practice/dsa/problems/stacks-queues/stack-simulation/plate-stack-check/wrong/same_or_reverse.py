class Solution:
    # Mistake: only accepts serving in the washing order or its exact reverse.
    def couldHappen(self, washed, served):
        return served == washed or served == washed[::-1]
