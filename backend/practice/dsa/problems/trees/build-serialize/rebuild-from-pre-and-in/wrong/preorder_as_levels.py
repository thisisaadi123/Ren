class Solution:
    # Mistake: fills the tree level by level from the pre-order list.
    def rebuild(self, preorder, inorder):
        nodes = [TreeNode(v) for v in preorder]
        for i, n in enumerate(nodes):
            if 2 * i + 1 < len(nodes):
                n.left = nodes[2 * i + 1]
            if 2 * i + 2 < len(nodes):
                n.right = nodes[2 * i + 2]
        return nodes[0]
