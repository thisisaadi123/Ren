class Solution:
    # Mistake: the middle element is only the majority after sorting.
    def majorityValue(self, readings):
        return readings[len(readings) // 2]
