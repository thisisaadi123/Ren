class Solution:
    def rebuildPrePost(self, preorder, postorder):
        if not preorder:
            return None
        node = TreeNode(preorder[0])
        if len(preorder) == 1:
            return node
        k = postorder.index(preorder[1]) + 1
        node.right = self.rebuildPrePost(preorder[1:k + 1], postorder[:k])
        node.left = self.rebuildPrePost(preorder[k + 1:], postorder[k:-1])
        if node.left and node.right:
            node.left, node.right = node.right, node.left
        return node
