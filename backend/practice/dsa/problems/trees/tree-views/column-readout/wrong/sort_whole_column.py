from collections import deque


class Solution:
    # Mistake: sorts each whole column by value, ignoring the rows.
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
        return [sorted(cols[c]) for c in sorted(cols)]
