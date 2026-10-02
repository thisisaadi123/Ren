class Solution:
    # Mistake: searches the in-order list and copies slices at every step: O(n^2) on a chain.
    def rebuildPost(self, inorder, postorder):
        def build(ino, post):
            if not post:
                return None
            v = post[-1]
            m = ino.index(v)
            return TreeNode(v, build(ino[:m], post[:m]), build(ino[m + 1:], post[m:-1]))

        return build(inorder, postorder)
