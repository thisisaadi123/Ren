class Solution:
    # Mistake: returns every match instead of at most three.
    def suggest(self, products, typed):
        products = sorted(products)
        return [[w for w in products if w.startswith(typed[:i])] for i in range(1, len(typed) + 1)]
