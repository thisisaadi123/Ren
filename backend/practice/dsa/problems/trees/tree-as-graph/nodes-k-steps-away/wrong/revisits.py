class Solution:
    # Mistake: forgets which nodes were visited, so walks can go back and forth.
    def kAway(self, root, start, k):
        adj = {}
        stack = [root]
        while stack:
            n = stack.pop()
            adj.setdefault(n.val, [])
            for c in (n.left, n.right):
                if c:
                    adj[n.val].append(c.val)
                    adj.setdefault(c.val, []).append(n.val)
                    stack.append(c)
        frontier = {start}
        for _ in range(k):
            frontier = {y for x in frontier for y in adj[x]}
        return sorted(frontier)
