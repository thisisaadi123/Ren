class Solution:
    # Mistake: returns the average instead of the median.
    def middleReading(self, readings):
        return sum(readings) // len(readings)
