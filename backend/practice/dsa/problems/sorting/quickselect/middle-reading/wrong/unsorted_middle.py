class Solution:
    # Mistake: takes the middle of the unsorted list.
    def middleReading(self, readings):
        return readings[len(readings) // 2]
