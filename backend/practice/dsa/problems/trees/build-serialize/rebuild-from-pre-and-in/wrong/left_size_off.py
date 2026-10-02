class Solution:
    # Mistake: gives the left subtree one node too many from the pre-order list.
    def rebuild(self, preorder, inorder):
        if not preorder:
            return None
        v = preorder[0]
        m = inorder.index(v)
        k = min(m + 1, len(preorder) - 1)
        return TreeNode(v, self.rebuild(preorder[1:k + 1], inorder[:m]), self.rebuild(preorder[k + 1:], inorder[m + 1:]))
