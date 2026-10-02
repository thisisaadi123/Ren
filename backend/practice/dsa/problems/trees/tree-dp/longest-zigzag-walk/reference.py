class Solution:
    def longestZigzag(self, root):
        best = 0
        stack = [(root, 0, 0)]  # node, how we arrived (-1 left, 1 right, 0 root), length
        while stack:
            n, came, length = stack.pop()
            best = max(best, length)
            if n.left:
                stack.append((n.left, -1, length + 1 if came == 1 else 1))
            if n.right:
                stack.append((n.right, 1, length + 1 if came == -1 else 1))
        return best
