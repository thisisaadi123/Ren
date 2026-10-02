class Solution:
    # Mistake: builds the left subtree first while reading post-order from the back.
    def rebuildPost(self, inorder, postorder):
        at = {v: i for i, v in enumerate(inorder)}
        pos = [len(postorder) - 1]

        def build(lo, hi):
            if lo > hi or pos[0] < 0:
                return None
            v = postorder[pos[0]]
            pos[0] -= 1
            m = at[v]
            node = TreeNode(v)
            node.left = build(lo, m - 1)
            node.right = build(m + 1, hi)
            return node

        return build(0, len(inorder) - 1)
