class Solution:
    # Mistake: drops a node outside the range together with everything below it.
    def trimPrices(self, root, low, high):
        def trim(node):
            if node is None or not low <= node.val <= high:
                return None
            node.left = trim(node.left)
            node.right = trim(node.right)
            return node

        return trim(root)
