class Solution:
    # Mistake: counts bloomed flowers in total, ignoring that a bouquet's flowers must be neighbours.
    def earliestBouquetDay(self, bloom, bouquets, size):
        need = bouquets * size
        if need > len(bloom):
            return -1
        return sorted(bloom)[need - 1]
