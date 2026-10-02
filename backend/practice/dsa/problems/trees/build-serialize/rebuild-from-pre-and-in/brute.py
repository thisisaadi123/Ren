class Solution:
    def rebuild(self, preorder, inorder):
        if not preorder:
            return None
        v = preorder[0]
        m = inorder.index(v)
        return TreeNode(v, self.rebuild(preorder[1:m + 1], inorder[:m]), self.rebuild(preorder[m + 1:], inorder[m + 1:]))
