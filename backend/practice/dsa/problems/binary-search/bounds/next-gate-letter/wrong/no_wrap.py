class Solution:
    # Mistake: returns the last gate instead of wrapping around.
    def nextGate(self, gates, current):
        for g in gates:
            if g > current:
                return g
        return gates[-1]
