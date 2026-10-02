class Solution:
    def nearestExit(self, root, start):
        parent, depth, leaves, stack = {root.val: None}, {root.val: 0}, [], [root]
        while stack:
            n = stack.pop()
            if not n.left and not n.right:
                leaves.append(n.val)
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

        return min(leaves, key=lambda v: (dist(start, v), v))
