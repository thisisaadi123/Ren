from collections import deque


class Solution:
    def hops(self, root, p, q):
        parent, depth = {root.val: None}, {root.val: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for c in (node.left, node.right):
                if c:
                    parent[c.val] = node.val
                    depth[c.val] = depth[node.val] + 1
                    queue.append(c)
        a, b = p, q
        while depth[a] > depth[b]:
            a = parent[a]
        while depth[b] > depth[a]:
            b = parent[b]
        while a != b:
            a, b = parent[a], parent[b]
        return depth[p] + depth[q] - 2 * depth[a]
