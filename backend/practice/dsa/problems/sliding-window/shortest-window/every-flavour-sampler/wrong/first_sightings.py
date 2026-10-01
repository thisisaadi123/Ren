class Solution:
    # Mistake: spans from the first sighting of any flavour to the first sighting of the last new one.
    def shortestSampler(self, jars):
        first = {}
        for i, f in enumerate(jars):
            first.setdefault(f, i)
        return max(first.values()) - min(first.values()) + 1
