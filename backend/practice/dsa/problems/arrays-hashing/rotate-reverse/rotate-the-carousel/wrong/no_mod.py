class Solution:
    # Mistake: forgets that k can be larger than n.
    def rotateRight(self, slots, k):
        n = len(slots)
        k = min(k, n)
        return slots[n - k:] + slots[:n - k]
