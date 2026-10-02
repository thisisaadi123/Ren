from bisect import bisect_left


class Solution:
    def suggest(self, products, typed):
        products = sorted(products)
        out = []
        for i in range(1, len(typed) + 1):
            p = typed[:i]
            k = bisect_left(products, p)
            out.append([w for w in products[k:k + 3] if w.startswith(p)])
        return out
