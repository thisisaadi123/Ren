class Solution:
    # Mistake: uses the global maximum as the water level everywhere.
    def trappedWater(self, walls):
        top = max(walls)
        first = walls.index(top)
        last = len(walls) - 1 - walls[::-1].index(top)
        return sum(top - w for w in walls[first:last + 1])
