class Solution:
    def trappedWater(self, walls):
        total = 0
        n = len(walls)
        for i in range(n):
            left = max(walls[: i + 1])
            right = max(walls[i:])
            total += min(left, right) - walls[i]
        return total
