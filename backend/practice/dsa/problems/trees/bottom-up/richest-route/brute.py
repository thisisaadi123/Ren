class Solution:
    def richestRoute(self, root):
        # Every route is the path between two caves u and v; try all pairs.
        parent, depth, nodes = {id(root): None}, {id(root): 0}, [root]
        for node in nodes:
            for c in (node.left, node.right):
                if c:
                    parent[id(c)] = node
                    depth[id(c)] = depth[id(node)] + 1
                    nodes.append(c)
        best = None
        for u in nodes:
            for v in nodes:
                a, b, s = u, v, 0
                while a is not b:
                    if depth[id(a)] >= depth[id(b)]:
                        s += a.val
                        a = parent[id(a)]
                    else:
                        s += b.val
                        b = parent[id(b)]
                s += a.val
                best = s if best is None else max(best, s)
        return best
