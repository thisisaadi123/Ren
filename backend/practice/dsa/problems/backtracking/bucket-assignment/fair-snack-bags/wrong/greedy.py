class Solution:
    # Mistake: gives each bag (biggest first) to the kid with the fewest snacks.
    def fairestSplit(self, bags, kids):
        load = [0] * kids
        for b in sorted(bags, reverse=True):
            load[load.index(min(load))] += b
        return max(load)
