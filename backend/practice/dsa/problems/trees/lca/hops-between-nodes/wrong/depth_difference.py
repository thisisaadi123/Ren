from collections import deque


class Solution:
    # Mistake: returns the difference in depth, as if one room were always above the other.
    def hops(self, root, p, q):
        depth = {root.val: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for c in (node.left, node.right):
                if c:
                    depth[c.val] = depth[node.val] + 1
                    queue.append(c)
        return abs(depth[p] - depth[q])
