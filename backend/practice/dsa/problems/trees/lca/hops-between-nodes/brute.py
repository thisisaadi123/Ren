from collections import deque


class Solution:
    def hops(self, root, p, q):
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
        dist = {p: 0}
        queue = deque([p])
        while queue:
            x = queue.popleft()
            for y in adj[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    queue.append(y)
        return dist[q]
