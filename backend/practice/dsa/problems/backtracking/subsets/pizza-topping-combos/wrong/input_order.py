class Solution:
    # Mistake: keeps codes in input order instead of increasing order.
    def toppingCombos(self, toppings):
        out, pick = [], []
        def go(i):
            if i == len(toppings):
                out.append(pick[:])
                return
            go(i + 1)
            pick.append(toppings[i])
            go(i + 1)
            pick.pop()
        go(0)
        return out
