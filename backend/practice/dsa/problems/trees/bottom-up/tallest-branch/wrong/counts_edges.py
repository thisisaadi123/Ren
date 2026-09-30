class Solution:
    # Mistake: counts links on the longest path instead of generations (off by one).
    def tallestBranch(self, root):
        def height(node):
            if node is None:
                return 0
            return 1 + max(height(node.left), height(node.right))

        return max(0, height(root) - 1)
