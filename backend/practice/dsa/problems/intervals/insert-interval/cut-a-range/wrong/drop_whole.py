class Solution:
    # Mistake: drops every slot the cut touches, instead of keeping the parts outside it.
    def cutRange(self, slots, cut):
        a, b = cut
        return [[s, e] for s, e in slots if e <= a or s >= b]
