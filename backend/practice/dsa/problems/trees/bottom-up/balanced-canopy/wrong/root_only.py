class Solution:
    # Mistake: compares the heights only at the root.
    def isBalanced(self, root):
        def h(node):
            d, level = 0, [node] if node else []
            while level:
                d += 1
                level = [c for x in level for c in (x.left, x.right) if c]
            return d

        return root is None or abs(h(root.left) - h(root.right)) <= 1
