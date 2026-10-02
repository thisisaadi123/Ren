from collections import deque


class Solution:
    def splitPoint(self, root, p, q):
        parent = {root.val: None}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for c in (node.left, node.right):
                if c:
                    parent[c.val] = node.val
                    queue.append(c)
        above = set()
        x = p
        while x is not None:
            above.add(x)
            x = parent[x]
        y = q
        while y not in above:
            y = parent[y]
        return y
