class Solution:
    # Recomputes both branch heights from scratch at every room: O(n^2) on a chain.
    def longestWalk(self, root):
        def h(node):
            d = 0
            stack = [(node, 1)] if node else []
            while stack:
                x, k = stack.pop()
                d = max(d, k)
                stack.extend((c, k + 1) for c in (x.left, x.right) if c)
            return d

        best, todo = 0, [root]
        while todo:
            node = todo.pop()
            best = max(best, h(node.left) + h(node.right))
            todo.extend(c for c in (node.left, node.right) if c)
        return best
