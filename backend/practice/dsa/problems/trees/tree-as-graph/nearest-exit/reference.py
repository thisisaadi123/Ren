class Solution:
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
            hits = [x for x in frontier if x in leaf]
            if hits:
                return min(hits)
            nxt = []
            for x in frontier:
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y)
                        nxt.append(y)
            frontier = nxt
