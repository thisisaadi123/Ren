class Solution:
    def bandTotal(self, root, low, high):
        def walk(node):
            if node is None:
                return 0
            here = node.val if low <= node.val <= high else 0
            return here + walk(node.left) + walk(node.right)

        return walk(root)
