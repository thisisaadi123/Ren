class Solution:
    # Mistake: forgets that people ahead may leave early, and multiplies the line length by k's tickets.
    def secondsToFinish(self, wants, k):
        return (wants[k] - 1) * len(wants) + k + 1
