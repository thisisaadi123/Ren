from collections import deque


class Solution:
    # Mistake: keeps nodes that share a row and column in level order instead of by value.
    def columnReadout(self, root):
        cols = {}
        queue = deque([(root, 0)])
        while queue:
            node, col = queue.popleft()
            cols.setdefault(col, []).append(node.val)
            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))
        return [cols[c] for c in sorted(cols)]
