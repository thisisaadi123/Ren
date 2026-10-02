from bisect import bisect_left


class Solution:
    # Mistake: stops adding lists once nothing matches, instead of adding empty lists for the rest.
    def suggest(self, products, typed):
        products = sorted(products)
        out = []
        for i in range(1, len(typed) + 1):
            p = typed[:i]
            k = bisect_left(products, p)
            hits = [w for w in products[k:k + 3] if w.startswith(p)]
            if not hits:
                break
            out.append(hits)
        return out
