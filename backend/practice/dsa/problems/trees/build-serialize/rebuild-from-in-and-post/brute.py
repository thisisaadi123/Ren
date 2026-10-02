class Solution:
    def rebuildPost(self, inorder, postorder):
        if not postorder:
            return None
        v = postorder[-1]
        m = inorder.index(v)
        return TreeNode(v, self.rebuildPost(inorder[:m], postorder[:m]), self.rebuildPost(inorder[m + 1:], postorder[m:-1]))
