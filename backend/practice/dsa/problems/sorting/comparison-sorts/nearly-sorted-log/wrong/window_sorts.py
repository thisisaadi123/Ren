class Solution:
    # Mistake: sorts fixed blocks of k items, which misses moves across block edges.
    def sortLog(self, times, k):
        a = times[:]
        size = max(1, k)
        for s in range(0, len(a), size):
            a[s:s + size] = sorted(a[s:s + size])
        return a
