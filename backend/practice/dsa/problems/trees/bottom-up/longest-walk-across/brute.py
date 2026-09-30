class Solution:
    def longestWalk(self, root):
        # Turn the tree into a graph and BFS from every room.
        adj, todo = {}, [root]
        while todo:
            node = todo.pop()
            adj.setdefault(id(node), [])
            for c in (node.left, node.right):
                if c:
                    adj[id(node)].append(id(c))
                    adj.setdefault(id(c), []).append(id(node))
                    todo.append(c)
        best = 0
        for s in adj:
            dist, q = {s: 0}, [s]
            for u in q:
                for v in adj[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        q.append(v)
            best = max(best, max(dist.values()))
        return best
