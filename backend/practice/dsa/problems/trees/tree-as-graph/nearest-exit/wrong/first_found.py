class Solution:
    # Mistake: returns the first leaf the search reaches instead of the smallest one at that distance.
    def nearestExit(self, root, start):
        adj, leaf = {}, set()
        stack = [root]
        while stack:
            n = stack.pop()
            adj.setdefault(n.val, [])
            if not n.left and not n.right:
                leaf.add(n.val)
            for c in (n.left, n.right):
                if c:
                    adj[n.val].append(c.val)
                    adj.setdefault(c.val, []).append(n.val)
                    stack.append(c)
        seen, frontier = {start}, [start]
        while frontier:
            for x in frontier:
                if x in leaf:
                    return x
            nxt = []
            for x in frontier:
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y)
                        nxt.append(y)
            frontier = nxt
