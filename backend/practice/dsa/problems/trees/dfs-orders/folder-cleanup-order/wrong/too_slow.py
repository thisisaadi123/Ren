class Solution:
    # Concatenates the children's lists at every folder: O(n^2) copying on a long chain.
    def cleanupOrder(self, root):
        def walk(node):
            if node is None:
                return []
            return walk(node.left) + walk(node.right) + [node.val]

        return walk(root)
