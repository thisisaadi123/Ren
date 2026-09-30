class Solution:
    # Mistake: visits the right branch before the left one (reversed shelf order).
    def shelfOrder(self, root):
        out = []

        def walk(node):
            if node:
                walk(node.right)
                out.append(node.val)
                walk(node.left)

        walk(root)
        return out
