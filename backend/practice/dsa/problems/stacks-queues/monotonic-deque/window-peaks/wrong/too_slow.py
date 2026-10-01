class Solution:
    # Mistake: scans every window: O(n * k).
    def windowPeaks(self, temps, k):
        out = []
        for i in range(len(temps) - k + 1):
            m = temps[i]
            for v in temps[i:i + k]:
                if v > m:
                    m = v
            out.append(m)
        return out
