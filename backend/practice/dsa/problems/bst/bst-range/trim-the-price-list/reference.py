class Solution:
    def trimPrices(self, root, low, high):
        while root and not low <= root.val <= high:
            root = root.right if root.val < low else root.left
        if root is None:
            return None
        node = root
        while node:
            while node.left and node.left.val < low:
                node.left = node.left.right
            node = node.left
        node = root
        while node:
            while node.right and node.right.val > high:
                node.right = node.right.left
            node = node.right
        return root
