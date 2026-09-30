class Solution:
    # Mistake: removes only the first blank.
    def removeValue(self, cells, blank):
        a = cells[:]
        if blank in a:
            a.remove(blank)
        return a
