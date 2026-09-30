class Solution:
    # Mistake: applies the loop formula even to steps that end before reaching the loop.
    def positionsAfter(self, head, steps):
        seen = {}
        vals = []
        node = head
        while node and node not in seen:
            seen[node] = len(vals)
            vals.append(node.val)
            node = node.next
        n = len(vals)
        if node is None:
            return [vals[s] if s < n else -1 for s in steps]
        mu = seen[node]
        lam = n - mu
        return [vals[mu + (s - mu) % lam] for s in steps]
