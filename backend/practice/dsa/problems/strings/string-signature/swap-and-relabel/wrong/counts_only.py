class Solution:
    # Mistake: compares only the sorted counts, forgetting that a relabel can't bring in a new letter.
    def canReshape(self, a, b):
        return sorted(collections.Counter(a).values()) == sorted(collections.Counter(b).values())
