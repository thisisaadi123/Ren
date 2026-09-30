class Solution:
    def isBalanced(self, root):
        def height(node):
            if node is None:
                return 0
            l = height(node.left)
            if l < 0:
                return -1
            r = height(node.right)
            if r < 0 or abs(l - r) > 1:
                return -1
            return 1 + max(l, r)

        return height(root) >= 0
