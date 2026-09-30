class Solution:
    def removeValue(self, cells, blank):
        return [x for x in cells if x != blank]
