class Solution:
    # Mistake: removes the empty slots instead of moving them.
    def compactShelf(self, slots):
        return [x for x in slots if x != 0]
