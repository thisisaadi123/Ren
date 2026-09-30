class Solution:
    # Mistake: returns the index after the first drop instead of before it.
    def mountainTop(self, elevations):
        for i in range(1, len(elevations)):
            if elevations[i] < elevations[i - 1]:
                return i
        return len(elevations) - 1
