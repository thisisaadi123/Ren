class Solution:
    def minutesToSpread(self, root, start):
        parent, depth, nodes, stack = {root.val: None}, {root.val: 0}, [], [root]
        while stack:
            n = stack.pop()
            nodes.append(n.val)
            for c in (n.left, n.right):
                if c:
                    parent[c.val] = n.val
                    depth[c.val] = depth[n.val] + 1
                    stack.append(c)

        def dist(a, b):
            x, y, steps = a, b, 0
            while depth[x] > depth[y]:
                x, steps = parent[x], steps + 1
            while depth[y] > depth[x]:
                y, steps = parent[y], steps + 1
            while x != y:
                x, y, steps = parent[x], parent[y], steps + 2
            return steps

        return max(dist(start, v) for v in nodes)
