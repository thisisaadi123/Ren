class Solution:
    # Mistake: loses repeated readings.
    def sortReadings(self, readings):
        return sorted(set(readings))
