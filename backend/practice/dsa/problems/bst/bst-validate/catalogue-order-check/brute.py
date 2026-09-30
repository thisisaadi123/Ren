class Solution:
    def isSearchTree(self, root):
        # In-order reading of a search tree is strictly increasing.
        seq = []

        def walk(node):
            if node:
                walk(node.left)
                seq.append(node.val)
                walk(node.right)

        walk(root)
        return all(a < b for a, b in zip(seq, seq[1:]))
