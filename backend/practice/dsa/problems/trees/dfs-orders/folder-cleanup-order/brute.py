class Solution:
    def cleanupOrder(self, root):
        out = []

        def walk(node):
            if node:
                walk(node.left)
                walk(node.right)
                out.append(node.val)

        walk(root)
        return out
