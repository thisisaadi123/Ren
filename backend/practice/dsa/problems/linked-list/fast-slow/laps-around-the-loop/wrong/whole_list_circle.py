class Solution:
    # Mistake: treats the whole list as the loop (index s mod n), ignoring the tail before the loop.
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
        return [vals[s % n] for s in steps]
