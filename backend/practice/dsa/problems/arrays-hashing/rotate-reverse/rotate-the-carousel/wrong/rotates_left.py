class Solution:
    # Mistake: turns the wrong way.
    def rotateRight(self, slots, k):
        k %= len(slots)
        return slots[k:] + slots[:k]
