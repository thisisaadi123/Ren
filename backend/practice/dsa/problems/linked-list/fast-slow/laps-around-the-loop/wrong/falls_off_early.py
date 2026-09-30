class Solution:
    # Mistake: without a loop, treats landing on the last node as falling off.
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
            return [vals[s] if s < n - 1 else -1 for s in steps]
        mu = seen[node]
        lam = n - mu
        return [vals[s] if s < n else vals[mu + (s - mu) % lam] for s in steps]
