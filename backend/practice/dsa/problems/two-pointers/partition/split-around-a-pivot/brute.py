class Solution:
    def splitAround(self, values, pivot):
        return [x for x in values if x < pivot] + [x for x in values if x == pivot] + [x for x in values if x > pivot]
