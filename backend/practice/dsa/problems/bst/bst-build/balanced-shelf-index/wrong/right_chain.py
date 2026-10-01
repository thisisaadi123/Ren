class Solution:
    # Mistake: links the codes into a right-leaning chain, which is a search tree but not balanced.
    def buildIndex(self, codes):
        root = None
        for v in reversed(codes):
            root = TreeNode(v, None, root)
        return root
