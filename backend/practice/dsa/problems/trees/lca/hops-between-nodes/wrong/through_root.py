from collections import deque


class Solution:
    # Mistake: always routes through the root.
    def hops(self, root, p, q):
        depth = {root.val: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for c in (node.left, node.right):
                if c:
                    depth[c.val] = depth[node.val] + 1
                    queue.append(c)
        return depth[p] + depth[q] if p != q else 0
