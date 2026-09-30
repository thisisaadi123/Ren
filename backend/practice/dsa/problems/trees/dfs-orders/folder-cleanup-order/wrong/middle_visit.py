class Solution:
    # Mistake: deletes the folder between its two branches (in-order).
    def cleanupOrder(self, root):
        out = []

        def walk(node):
            if node:
                walk(node.left)
                out.append(node.val)
                walk(node.right)

        walk(root)
        return out
