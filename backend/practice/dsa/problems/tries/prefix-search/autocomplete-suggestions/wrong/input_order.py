class Solution:
    # Mistake: suggests the first three matches in the given order, not the alphabetically smallest.
    def suggest(self, products, typed):
        return [[w for w in products if w.startswith(typed[:i])][:3] for i in range(1, len(typed) + 1)]
