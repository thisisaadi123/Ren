class Solution:
    def trappedWater(self, walls):
        total = 0
        for i in range(len(walls)):
            level = min(max(walls[: i + 1]), max(walls[i:]))
            total += level - walls[i]
        return total
