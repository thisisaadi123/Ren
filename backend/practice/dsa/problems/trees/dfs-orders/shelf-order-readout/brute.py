class Solution:
    def shelfOrder(self, root):
        out = []

        def walk(node):
            if node:
                walk(node.left)
                out.append(node.val)
                walk(node.right)

        walk(root)
        return out
