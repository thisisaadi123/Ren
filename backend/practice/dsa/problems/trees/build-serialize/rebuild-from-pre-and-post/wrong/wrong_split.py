class Solution:
    # Mistake: sizes the first subtree from preorder[1]'s position in post-order without the + 1.
    def rebuildPrePost(self, preorder, postorder):
        if not preorder:
            return None
        node = TreeNode(preorder[0])
        if len(preorder) == 1:
            return node
        k = max(1, postorder.index(preorder[1]))
        node.left = self.rebuildPrePost(preorder[1:k + 1], postorder[:k])
        node.right = self.rebuildPrePost(preorder[k + 1:], postorder[k:-1])
        return node
