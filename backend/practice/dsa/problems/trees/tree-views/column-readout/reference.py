from collections import deque


class Solution:
    def columnReadout(self, root):
        cells = []
        queue = deque([(root, 0, 0)])
        while queue:
            node, row, col = queue.popleft()
            cells.append((col, row, node.val))
            if node.left:
                queue.append((node.left, row + 1, col - 1))
            if node.right:
                queue.append((node.right, row + 1, col + 1))
        cells.sort()
        out, last = [], None
        for col, _, val in cells:
            if col != last:
                out.append([])
                last = col
            out[-1].append(val)
        return out
