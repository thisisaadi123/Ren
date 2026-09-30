class Solution:
    def smallestDivisor(self, loads, threshold):
        d = 1
        while sum((x + d - 1) // d for x in loads) > threshold:
            d += 1
        return d
