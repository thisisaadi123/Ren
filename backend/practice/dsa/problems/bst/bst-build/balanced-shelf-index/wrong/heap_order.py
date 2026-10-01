class Solution:
    # Mistake: fills the tree level by level in sorted order: balanced, but not a search tree.
    def buildIndex(self, codes):
        nodes = [TreeNode(v) for v in codes]
        for i, node in enumerate(nodes):
            if 2 * i + 1 < len(nodes):
                node.left = nodes[2 * i + 1]
            if 2 * i + 2 < len(nodes):
                node.right = nodes[2 * i + 2]
        return nodes[0]
