from collections import deque


class Solution:
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
        seen = {start}
        frontier = [start]
        for _ in range(k):
            nxt = []
            for x in frontier:
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y)
                        nxt.append(y)
            frontier = nxt
            if not frontier:
                break
        return sorted(frontier)
