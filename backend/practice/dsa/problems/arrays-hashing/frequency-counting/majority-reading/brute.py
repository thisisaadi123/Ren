class Solution:
    def majorityValue(self, readings):
        for r in readings:
            if readings.count(r) * 2 > len(readings):
                return r
