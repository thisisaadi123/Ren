class Solution:
    def toppingCombos(self, toppings):
        n = len(toppings)
        out = []
        for mask in range(1 << n):
            out.append(sorted(toppings[i] for i in range(n) if mask >> i & 1))
        return out
