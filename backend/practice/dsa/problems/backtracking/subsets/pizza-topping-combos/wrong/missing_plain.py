class Solution:
    # Mistake: only records non-empty picks, so the plain pizza (empty set) is missing.
    def toppingCombos(self, toppings):
        items = sorted(toppings)
        out, pick = [], []
        def go(i):
            if i == len(items):
                if pick:
                    out.append(pick[:])
                return
            go(i + 1)
            pick.append(items[i])
            go(i + 1)
            pick.pop()
        go(0)
        return out
