class Solution:
    # Mistake: hangs every value off the previous one in pre-order, ignoring branching.
    def rebuildPrePost(self, preorder, postorder):
        root = TreeNode(preorder[0])
        cur = root
        for v in preorder[1:]:
            cur.left = TreeNode(v)
            cur = cur.left
        return root
