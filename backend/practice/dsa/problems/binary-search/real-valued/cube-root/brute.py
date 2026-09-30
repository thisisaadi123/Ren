class Solution:
    def cubeRoot(self, volume):
        return math.copysign(abs(volume) ** (1.0 / 3.0), volume)
