class Solution:
    def trimPrices(self, root, low, high):
        def trim(node):
            if node is None:
                return None
            if node.val < low:
                return trim(node.right)
            if node.val > high:
                return trim(node.left)
            node.left = trim(node.left)
            node.right = trim(node.right)
            return node

        return trim(root)
