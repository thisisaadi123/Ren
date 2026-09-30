class Solution:
    def nextGate(self, gates, current):
        for g in gates:
            if g > current:
                return g
        return gates[0]
