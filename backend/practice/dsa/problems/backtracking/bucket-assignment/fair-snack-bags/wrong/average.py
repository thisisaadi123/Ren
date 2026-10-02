class Solution:
    # Mistake: assumes the snacks can always be split evenly.
    def fairestSplit(self, bags, kids):
        return max(max(bags), -(-sum(bags) // kids))
