class Solution:
    # Mistake: keeps each value only once.
    def keepAtMostTwo(self, values):
        return sorted(set(values))
