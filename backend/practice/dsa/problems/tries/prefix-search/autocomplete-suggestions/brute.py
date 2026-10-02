class Solution:
    def suggest(self, products, typed):
        return [sorted(w for w in products if w.startswith(typed[:i]))[:3] for i in range(1, len(typed) + 1)]
