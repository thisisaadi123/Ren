class Solution:
    def windowPeaks(self, temps, k):
        return [max(temps[i:i + k]) for i in range(len(temps) - k + 1)]
