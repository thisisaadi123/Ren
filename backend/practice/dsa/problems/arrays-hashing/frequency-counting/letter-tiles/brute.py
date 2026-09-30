class Solution:
    def canSpell(self, sign, tiles):
        pool = list(tiles)
        for ch in sign:
            if ch not in pool:
                return False
            pool.remove(ch)
        return True
