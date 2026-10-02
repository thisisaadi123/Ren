from collections import deque


class Solution:
    # Mistake: keeps the LAST node seen in each column (the view from below).
    def topView(self, root):
        top = {}
        queue = deque([(root, 0)])
        while queue:
            node, col = queue.popleft()
            top[col] = node.val
            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))
        return [top[c] for c in sorted(top)]
