class Solution:
    def trappedWater(self, walls):
        lo, hi = 0, len(walls) - 1
        left_max = right_max = 0
        total = 0
        while lo < hi:
            if walls[lo] < walls[hi]:
                left_max = max(left_max, walls[lo])
                total += left_max - walls[lo]
                lo += 1
            else:
                right_max = max(right_max, walls[hi])
                total += right_max - walls[hi]
                hi -= 1
        return total
