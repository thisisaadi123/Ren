class Solution:
    def hasDuplicate(self, badges):
        seen = set()
        for b in badges:
            if b in seen:
                return True
            seen.add(b)
        return False
