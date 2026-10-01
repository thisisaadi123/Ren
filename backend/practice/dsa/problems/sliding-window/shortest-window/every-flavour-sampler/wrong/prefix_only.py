class Solution:
    # Mistake: only tries stretches that start at the first jar.
    def shortestSampler(self, jars):
        d = len(set(jars))
        seen = set()
        for i, f in enumerate(jars):
            seen.add(f)
            if len(seen) == d:
                return i + 1
