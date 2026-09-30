class Solution:
    def canSpell(self, sign, tiles):
        have = collections.Counter(tiles)
        for ch in sign:
            have[ch] -= 1
            if have[ch] < 0:
                return False
        return True
