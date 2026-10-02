class Solution:
    # Mistake: searches the in-order list and copies slices at every step: O(n^2) on a chain.
    def rebuild(self, preorder, inorder):
        def build(pre, ino):
            if not pre:
                return None
            v = pre[0]
            m = ino.index(v)
            return TreeNode(v, build(pre[1:m + 1], ino[:m]), build(pre[m + 1:], ino[m + 1:]))

        return build(preorder, inorder)
