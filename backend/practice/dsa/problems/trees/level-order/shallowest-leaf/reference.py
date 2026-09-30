class Solution:
    def shallowestLeaf(self, root):
        if not root:
            return 0
        queue = collections.deque([(root, 1)])
        while queue:
            node, d = queue.popleft()
            if not node.left and not node.right:
                return d
            for c in (node.left, node.right):
                if c:
                    queue.append((c, d + 1))
