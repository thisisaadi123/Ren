class Solution:
    # Mistake: keeps the first node a depth-first walk meets in each column, which may be a deeper one.
    def topView(self, root):
        top = {}
        stack = [(root, 0)]
        while stack:
            node, col = stack.pop()
            if col not in top:
                top[col] = node.val
            if node.right:
                stack.append((node.right, col + 1))
            if node.left:
                stack.append((node.left, col - 1))
        return [top[c] for c in sorted(top)]
