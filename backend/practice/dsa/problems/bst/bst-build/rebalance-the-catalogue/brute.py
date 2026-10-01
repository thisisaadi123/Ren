class Solution:
    def rebalance(self, root):
        vals = []

        def walk(node):
            if node:
                vals.append(node.val)
                walk(node.left)
                walk(node.right)

        walk(root)
        vals.sort()

        def build(part):
            if not part:
                return None
            mid = (len(part) - 1) // 2
            return TreeNode(part[mid], build(part[:mid]), build(part[mid + 1:]))

        return build(vals)
