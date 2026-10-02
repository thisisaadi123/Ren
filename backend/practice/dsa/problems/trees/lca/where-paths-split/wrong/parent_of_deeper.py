from collections import deque


class Solution:
    # Mistake: walks up from q only until it reaches p's depth, then returns that node.
    def splitPoint(self, root, p, q):
        parent, depth = {root.val: None}, {root.val: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for c in (node.left, node.right):
                if c:
                    parent[c.val] = node.val
                    depth[c.val] = depth[node.val] + 1
                    queue.append(c)
        a, b = (p, q) if depth[p] <= depth[q] else (q, p)
        while depth[b] > depth[a]:
            b = parent[b]
        return b
