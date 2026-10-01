class Solution:
    # Mistake: gives the people behind k a full extra round too.
    def secondsToFinish(self, wants, k):
        return sum(min(w, wants[k]) for w in wants)
