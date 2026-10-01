class Solution:
    # Mistake: keeps a running maximum that never drops readings that left the window.
    def windowPeaks(self, temps, k):
        best = None
        out = []
        for i, v in enumerate(temps):
            best = v if best is None else max(best, v)
            if i >= k - 1:
                out.append(best)
        return out
