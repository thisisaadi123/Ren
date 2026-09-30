class Solution:
    # Mistake: sorts the items instead of keeping their order.
    def compactShelf(self, slots):
        items = sorted(x for x in slots if x != 0)
        return items + [0] * (len(slots) - len(items))
