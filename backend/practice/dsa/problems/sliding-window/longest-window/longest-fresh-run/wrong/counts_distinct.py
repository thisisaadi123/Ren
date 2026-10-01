class Solution:
    # Mistake: returns how many different characters appear, not the longest fresh run.
    def longestFresh(self, s):
        return len(set(s))
