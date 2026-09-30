class Solution:
    # Mistake: only checks that each letter exists, not how many times.
    def canSpell(self, sign, tiles):
        return set(sign) <= set(tiles)
