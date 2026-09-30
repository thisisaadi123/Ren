class Solution:
    # Mistake: replaces a too-cheap node with its left side (which is even cheaper).
    def trimPrices(self, root, low, high):
        def trim(node):
            if node is None:
                return None
            if node.val < low:
                return trim(node.left)
            if node.val > high:
                return trim(node.right)
            node.left = trim(node.left)
            node.right = trim(node.right)
            return node

        return trim(root)
