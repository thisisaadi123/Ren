class Solution:
    def rebuildPost(self, inorder, postorder):
        at = {v: i for i, v in enumerate(inorder)}
        pos = [len(postorder) - 1]

        def build(lo, hi):
            if lo > hi:
                return None
            v = postorder[pos[0]]
            pos[0] -= 1
            m = at[v]
            node = TreeNode(v)
            node.right = build(m + 1, hi)
            node.left = build(lo, m - 1)
            return node

        return build(0, len(inorder) - 1)
