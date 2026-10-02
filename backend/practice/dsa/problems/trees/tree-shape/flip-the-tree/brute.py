class Solution:
    def flip(self, root):
        if not root:
            return None
        return TreeNode(root.val, self.flip(root.right), self.flip(root.left))
