class Solution:
    def toppingCombos(self, toppings):
        items = sorted(toppings)
        out, pick = [], []

        def go(i):
            if i == len(items):
                out.append(pick[:])
                return
            go(i + 1)
            pick.append(items[i])
            go(i + 1)
            pick.pop()

        go(0)
        return sorted(out)
