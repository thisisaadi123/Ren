import itertools
class Solution:
    def trimReading(self, num, k):
        best = None
        for keep in itertools.combinations(range(len(num)), len(num) - k):
            v = int("".join(num[i] for i in keep) or "0")
            if best is None or v < best:
                best = v
        return str(best)
