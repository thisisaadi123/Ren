class Solution:
    def minutesToSpread(self, root, start):
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
        seen, frontier, minutes = {start}, [start], -1
        while frontier:
            minutes += 1
            nxt = []
            for x in frontier:
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y)
                        nxt.append(y)
            frontier = nxt
        return minutes
