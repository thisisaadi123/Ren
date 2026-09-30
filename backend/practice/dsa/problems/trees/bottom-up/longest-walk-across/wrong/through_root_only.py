class Solution:
    # Mistake: only considers walks that pass through the root.
    def longestWalk(self, root):
        def h(node):
            d, level = 0, [node] if node else []
            while level:
                d += 1
                level = [c for x in level for c in (x.left, x.right) if c]
            return d

        return h(root.left) + h(root.right)
