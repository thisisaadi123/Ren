class Solution:
    def flattenToSpine(self, root):
        order = []

        def walk(node):
            if node:
                order.append(node.val)
                walk(node.left)
                walk(node.right)

        walk(root)
        head = None
        for v in reversed(order):
            head = TreeNode(v, None, head)
        return head
