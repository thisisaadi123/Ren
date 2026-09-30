class Solution:
    def tallestBranch(self, root):
        def height(node):
            if node is None:
                return 0
            return 1 + max(height(node.left), height(node.right))

        return height(root)
