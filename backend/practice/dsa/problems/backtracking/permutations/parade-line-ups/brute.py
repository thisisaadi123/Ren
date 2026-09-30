class Solution:
    def lineUps(self, floats):
        # Insert each new float into every gap of every order built so far.
        orders = [[]]
        for f in floats:
            orders = [o[:i] + [f] + o[i:] for o in orders for i in range(len(o) + 1)]
        return orders
