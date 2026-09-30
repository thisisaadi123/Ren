class Solution:
    # Mistake: returns the current gate's own letter when it's open.
    def nextGate(self, gates, current):
        for g in gates:
            if g >= current:
                return g
        return gates[0]
