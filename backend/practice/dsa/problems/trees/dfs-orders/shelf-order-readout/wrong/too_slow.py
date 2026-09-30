class Solution:
    # Builds a fresh list at every node by concatenation: O(n^2) copying on a long chain.
    def shelfOrder(self, root):
        def walk(node):
            if node is None:
                return []
            return walk(node.left) + [node.val] + walk(node.right)

        return walk(root)
