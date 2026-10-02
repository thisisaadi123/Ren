class Solution:
    # Mistake: treats the first post-order value as the root, as in a pre-order walk.
    def rebuildPost(self, inorder, postorder):
        if not postorder:
            return None
        v = postorder[0]
        m = inorder.index(v)
        return TreeNode(v, self.rebuildPost(inorder[:m], postorder[1:m + 1]), self.rebuildPost(inorder[m + 1:], postorder[m + 1:]))
