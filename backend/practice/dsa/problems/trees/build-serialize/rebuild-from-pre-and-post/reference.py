class Solution:
    def rebuildPrePost(self, preorder, postorder):
        at = {v: i for i, v in enumerate(postorder)}
        pos = [0]

        def build(lo, hi):
            # Builds the subtree whose post-order range is [lo, hi].
            v = preorder[pos[0]]
            pos[0] += 1
            node = TreeNode(v)
            if lo < hi:
                m = at[preorder[pos[0]]]
                node.left = build(lo, m)
                if m + 1 <= hi - 1:
                    node.right = build(m + 1, hi - 1)
            return node

        return build(0, len(postorder) - 1)
