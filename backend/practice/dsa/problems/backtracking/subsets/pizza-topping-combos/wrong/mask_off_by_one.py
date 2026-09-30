class Solution:
    # Mistake: stops the mask loop one early, so the set with every topping is missing.
    def toppingCombos(self, toppings):
        n = len(toppings)
        return [sorted(toppings[i] for i in range(n) if m >> i & 1) for m in range((1 << n) - 1)]
