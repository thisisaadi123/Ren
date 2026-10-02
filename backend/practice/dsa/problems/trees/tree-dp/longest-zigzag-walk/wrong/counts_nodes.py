class Solution:
    # Mistake: counts the nodes on the walk instead of the edges.
    def longestZigzag(self, root):
        best = 0
        stack = [(root, 0, 1)]
        while stack:
            n, came, length = stack.pop()
            best = max(best, length)
            if n.left:
                stack.append((n.left, -1, length + 1 if came == 1 else 2))
            if n.right:
                stack.append((n.right, 1, length + 1 if came == -1 else 2))
        return best
