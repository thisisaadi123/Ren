class Solution:
    def compactShelf(self, slots):
        items = [x for x in slots if x != 0]
        return items + [0] * (len(slots) - len(items))
