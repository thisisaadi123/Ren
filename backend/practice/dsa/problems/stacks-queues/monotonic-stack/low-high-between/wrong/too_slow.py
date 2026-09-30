class Solution:
    # Mistake: for each middle, scans everything to its right: O(n²).
    def hasLowHighBetween(self, values):
        low = float("inf")
        n = len(values)
        for j in range(n):
            if low < values[j]:
                for k in range(j + 1, n):
                    if low < values[k] < values[j]:
                        return True
            low = min(low, values[j])
        return False
