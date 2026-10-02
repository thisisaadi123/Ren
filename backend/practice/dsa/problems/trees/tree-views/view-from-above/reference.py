from collections import deque


class Solution:
    def topView(self, root):
        top = {}
        queue = deque([(root, 0)])
        while queue:
            node, col = queue.popleft()
            if col not in top:
                top[col] = node.val
            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))
        return [top[c] for c in sorted(top)]
